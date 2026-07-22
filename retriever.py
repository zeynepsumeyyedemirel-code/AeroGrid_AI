import os
import chromadb
from sentence_transformers import SentenceTransformer
from pypdf import PdfReader

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

print("🔍 AeroGrid RAG Engine: Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

chroma_client = chromadb.PersistentClient(path=DB_DIR)

collection_name = "aerogrid_knowledge_base"
try:
    chroma_client.delete_collection(name=collection_name)
except Exception:
    pass

collection = chroma_client.create_collection(
    name=collection_name,
    metadata={"hnsw:space": "cosine"}
)

def intelligent_chunk_text(text, max_chunk_size=400):
    raw_paragraphs = text.split("\n\n")
    chunks = []
    
    for para in raw_paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if len(para) <= max_chunk_size:
            chunks.append(para)
        else:
            lines = para.split("\n")
            current_chunk = ""
            for line in lines:
                if len(current_chunk) + len(line) <= max_chunk_size:
                    current_chunk += line + "\n"
                else:
                    if current_chunk.strip():
                        chunks.append(current_chunk.strip())
                    current_chunk = line + "\n"
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
                
    return chunks

def extract_text_from_file(file_path):
    """Extracts raw text from .txt and .pdf files."""
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n\n"
        except Exception as e:
            print(f"⚠️ Error reading PDF {file_path}: {e}")
            
    return text

def build_vector_store():
    documents = []
    metadatas = []
    ids = []
    
    doc_count = 0
    chunk_counter = 0

    print("📂 Indexing documents (.txt & .pdf) into ChromaDB...")
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".txt") or file.endswith(".pdf"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, DOCS_DIR)
                
                content = extract_text_from_file(file_path)
                if not content.strip():
                    continue

                chunks = intelligent_chunk_text(content)
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({"source": rel_path, "chunk_id": i})
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
        print(f"✅ Successfully indexed {len(documents)} knowledge chunks from {doc_count} files into ChromaDB!")
    else:
        print("⚠️ No valid documents found in 'docs/' directory.")

build_vector_store()

def retrieve_context(query, top_k=3):
    """Retrieves top_k chunks along with metadata and similarity score %."""
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
            # Convert cosine distance to similarity score percentage
            similarity_pct = round(max(0, (1 - dist)) * 100, 1)
            formatted_matches.append({
                "source": m['source'],
                "content": doc,
                "score": similarity_pct
            })
            
    return formatted_matches

if __name__ == "__main__":
    print("\n🔎 Testing ChromaDB Retrieval Engine with Scores...")
    matches = retrieve_context("What is the maximum wind speed limit for climbing?", top_k=2)
    for i, match in enumerate(matches, 1):
        print(f"\n--- Match {i} (Source: {match['source']} | Score: {match['score']}%) ---")
        print(match['content'])
