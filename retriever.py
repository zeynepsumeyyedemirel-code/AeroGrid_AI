import os
import hashlib
import logging
from datetime import datetime
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

# --- Logging Setup ---
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AeroGrid_Retriever")

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

_model = None

def get_embedding_model():
    """Lazy loading for SentenceTransformer model to optimize import speed."""
    global _model
    if _model is None:
        logger.info("Loading SentenceTransformer embedding model (all-MiniLM-L6-v2)...")
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def get_chroma_collection():
    """Persistent client with lazy collection initialization."""
    chroma_client = chromadb.PersistentClient(path=DB_DIR)
    return chroma_client.get_or_create_collection(
        name="aerogrid_knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )

def compute_file_hash(file_path):
    """Computes SHA-256 hash of a file to track content changes."""
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        logger.error(f"Failed to compute SHA-256 hash for {file_path}: {e}")
        return None

def intelligent_chunk_text(text, max_chunk_size=400, overlap=50):
    """Recursive chunking with character overlap to preserve semantic context."""
    raw_paragraphs = text.split("\n\n")
    chunks = []
    
    for para in raw_paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if len(para) <= max_chunk_size:
            chunks.append(para)
        else:
            start = 0
            while start < len(para):
                end = start + max_chunk_size
                chunk = para[start:end]
                chunks.append(chunk.strip())
                start += max_chunk_size - overlap
                if start >= len(para) - overlap:
                    break
                    
    return chunks

def extract_text_from_file(file_path):
    """Extracts raw text and page-level details from .txt and .pdf files."""
    ext = os.path.splitext(file_path)[1].lower()
    extracted_pages = []
    
    if ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                extracted_pages.append((1, f.read()))
        except Exception as e:
            logger.error(f"Error reading TXT file {file_path}: {e}")
            
    elif ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            for page_num, page in enumerate(reader.pages, 1):
                extracted = page.extract_text()
                if extracted:
                    extracted_pages.append((page_num, extracted))
        except Exception as e:
            logger.error(f"Error reading PDF file {file_path}: {e}")
            
    return extracted_pages

def build_vector_store(force_reindex=False):
    """Incremental indexing tracking file SHA-256 hashes and detailed metadata."""
    collection = get_chroma_collection()
    model = get_embedding_model()
    
    # Map existing files to their indexed SHA-256 hashes
    existing_hashes = {}
    if not force_reindex:
        existing_records = collection.get(include=["metadatas"])
        if existing_records and "metadatas" in existing_records:
            for meta in existing_records["metadatas"]:
                if meta and "source" in meta and "file_hash" in meta:
                    existing_hashes[meta["source"]] = meta["file_hash"]

    documents = []
    metadatas = []
    ids = []
    
    doc_count = 0
    chunk_counter = collection.count()

    logger.info("Checking knowledge base documents for incremental indexing...")
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".txt") or file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, DOCS_DIR)
                file_hash = compute_file_hash(file_path)
                file_size = os.path.getsize(file_path)
                
                # Check if file is already indexed with identical content hash
                if not force_reindex and rel_path in existing_hashes and existing_hashes[rel_path] == file_hash:
                    continue

                pages_data = extract_text_from_file(file_path)
                if not pages_data:
                    logger.warning(f"File skipped or empty: {rel_path}")
                    continue

                for page_num, content in pages_data:
                    chunks = intelligent_chunk_text(content, max_chunk_size=400, overlap=50)
                    for i, chunk in enumerate(chunks):
                        documents.append(chunk)
                        metadatas.append({
                            "source": rel_path,
                            "page": page_num,
                            "chunk_id": i,
                            "file_hash": file_hash,
                            "file_size_bytes": file_size,
                            "created_at": datetime.now().isoformat()
                        })
                        ids.append(f"doc_{chunk_counter}")
                        chunk_counter += 1
                doc_count += 1

    if documents:
        embeddings = model.encode(documents).tolist()
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Successfully added {len(documents)} new chunks from {doc_count} files into ChromaDB.")
    else:
        logger.info("ChromaDB is up-to-date. No new or modified documents detected.")

def retrieve_context(query, top_k=3):
    """Retrieves top_k relevant chunks with enriched metadata and similarity score %."""
    collection = get_chroma_collection()
    model = get_embedding_model()
    
    logger.info(f"Retrieving context for query: '{query}' (top_k={top_k})")
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    formatted_matches = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        meta = results["metadatas"][0]
        distances = results["distances"][0] if "distances" in results else [0.0]*len(docs)
        
        for doc, m, dist in zip(docs, meta, distances):
            similarity_pct = round(max(0, (1 - dist)) * 100, 1)
            formatted_matches.append({
                "source": m.get('source', 'Unknown'),
                "page": m.get('page', 1),
                "chunk_id": m.get('chunk_id', 0),
                "content": doc,
                "score": similarity_pct
            })
            
    return formatted_matches

if __name__ == "__main__":
    logger.info("Initializing AeroGrid Knowledge Base directly...")
    build_vector_store()
    matches = retrieve_context("What is the maximum wind speed limit for climbing?", top_k=2)
    for i, match in enumerate(matches, 1):
        print(f"\n--- Match {i} (Source: {match['source']} | Page: {match['page']} | Score: {match['score']}%) ---")
        print(match['content'])
