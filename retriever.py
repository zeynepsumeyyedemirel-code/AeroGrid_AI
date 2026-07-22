import os
import chromadb
from sentence_transformers import SentenceTransformer

# 1. Initialize Vector Database & Embedding Model
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
DB_DIR = os.path.join(os.path.dirname(__file__), "chroma_db")

print("🔍 AeroGrid RAG Engine: Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Setup Persistent ChromaDB Client
chroma_client = chromadb.PersistentClient(path=DB_DIR)

# Reset / Get Collection
collection_name = "aerogrid_knowledge_base"
try:
    chroma_client.delete_collection(name=collection_name)
except Exception:
    pass

collection = chroma_client.create_collection(name=collection_name)

def intelligent_chunk_text(text, max_chunk_size=400):
    """
    Splits text by headers, blank lines, and procedure steps to maintain logical context.
    """
    raw_paragraphs = text.split("\n\n")
    chunks = []
    
    for para in raw_paragraphs:
        para = para.strip()
        if not para:
            continue
            
        # If paragraph is within limit, keep intact
        if len(para) <= max_chunk_size:
            chunks.append(para)
        else:
            # Sub-split long lists/procedures by lines
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

def build_vector_store():
    """Reads all text files in docs/ and stores embeddings in ChromaDB."""
    documents = []
    metadatas = []
    ids = []
    
    doc_count = 0
    chunk_counter = 0

    print("📂 Indexing documents into ChromaDB...")
    for root, _, files in os.walk(DOCS_DIR):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                rel_path = os.path.relpath(file_path, DOCS_DIR)
                
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                chunks = intelligent_chunk_text(content)
                for i, chunk in enumerate(chunks):
                    documents.append(chunk)
                    metadatas.append({"source": rel_path, "chunk_id": i})
                    ids.append(f"doc_{chunk_counter}")
                    chunk_counter += 1
                doc_count += 1

    if documents:
        # Generate embeddings & insert into ChromaDB
        embeddings = model.encode(documents).tolist()
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"✅ Successfully indexed {len(documents)} knowledge chunks from {doc_count} files into ChromaDB!")
    else:
        print("⚠️ No text files found in 'docs/' directory.")

# Run indexing on load
build_vector_store()

def retrieve_context(query, top_k=3):
    """Retrieves top_k most relevant chunks using ChromaDB query."""
    query_embedding = model.encode([query]).tolist()
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=top_k
    )

    formatted_matches = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        meta = results["metadatas"][0]
        
        for doc, m in zip(docs, meta):
            formatted_matches.append(f"Source: {m['source']}\n{doc}")
            
    return formatted_matches

if __name__ == "__main__":
    print("\n🔎 Testing ChromaDB Retrieval Engine...")
    test_query = "What is the maximum wind speed limit for climbing?"
    matches = retrieve_context(test_query, top_k=2)
    
    for i, match in enumerate(matches, 1):
        print(f"\n--- Match {i} ({match.splitlines()[0]}) ---")
        print("\n".join(match.splitlines()[1:]))
