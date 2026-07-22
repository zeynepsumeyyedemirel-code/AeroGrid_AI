import os
from sentence_transformers import SentenceTransformer
import numpy as np

class AeroGridRetriever:
    def __init__(self, docs_dir="docs"):
        self.docs_dir = docs_dir
        print("🔍 AeroGrid RAG Engine: Loading embedding model...")
        # Hafif ve hızlı Türkçe/İngilizce uyumlu vektör modeli
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.doc_embeddings = []
        self._load_and_embed_docs()

    def _load_and_embed_docs(self):
        if not os.path.exists(self.docs_dir):
            print(f"⚠️ Warning: '{self.docs_dir}' directory not found!")
            return

        print(f"📂 Indexing documents inside '{self.docs_dir}' (including subdirectories)...")
        
        # os.walk kullanarak docs/ altındaki tüm klasörleri ve .txt dosyalarını tarıyoruz
        for root, _, files in os.walk(self.docs_dir):
            for file_name in files:
                if file_name.endswith(".txt"):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # Metinleri paragraflara bölerek indeksliyoruz
                        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
                        
                        # Kaynak adı olarak göreceli yolu (relative path) alıyoruz (örn: wind_turbine/E-101-pitch-control.txt)
                        rel_source = os.path.relpath(file_path, self.docs_dir)
                        
                        for p in paragraphs:
                            self.documents.append({
                                "source": rel_source,
                                "text": p
                            })

        if self.documents:
            texts = [doc["text"] for doc in self.documents]
            self.doc_embeddings = self.embedder.encode(texts, convert_to_numpy=True)
            print(f"✅ Successfully indexed {len(self.documents)} knowledge chunks!")
        else:
            print("⚠️ No valid .txt documents found in 'docs/' folder.")

    def search(self, query, top_k=2):
        if not self.documents:
            return []

        query_embedding = self.embedder.encode([query], convert_to_numpy=True)
        # Cosine similarity hesaplama
        similarities = np.dot(self.doc_embeddings, query_embedding.T).squeeze()
        
        if np.ndim(similarities) == 0:
            top_indices = [0]
        else:
            top_indices = np.argsort(similarities)[::-1][:top_k]

        results = []
        for idx in top_indices:
            results.append(self.documents[idx])
        return results

if __name__ == "__main__":
    retriever = AeroGridRetriever()
    test_query = "What is the maximum wind speed limit for climbing?"
    print(f"\n🔎 Testing Search Query: '{test_query}'")
    matches = retriever.search(test_query)
    for i, match in enumerate(matches, 1):
        print(f"\n--- Match {i} (Source: {match['source']}) ---")
        print(match['text'])