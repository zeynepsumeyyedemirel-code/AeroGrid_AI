# 🛸 AeroGrid AI — Enterprise Renewable Energy Maintenance RAG Engine

AeroGrid AI is a production-grade, containerized Retrieval-Augmented Generation (RAG) system engineered for wind turbine and solar panel field maintenance technicians.

## 📊 Evaluation & Benchmark Metrics

| Metric Category | Specification / Score |
| :--- | :--- |
| **Evaluation Dataset** | 15 Synthetic Field Maintenance Protocols & Safety Docs |
| **Embedding Model** | sentence-transformers/all-MiniLM-L6-v2 |
| **Reranker Model** | cross-encoder/ms-marco-MiniLM-L-6-v2 |
| **LLM Engine** | Ollama (llama3.2 / Local LLM) |
| **Retrieval Precision@3** | 100.00% |
| **Unit Test Coverage** | 5/5 PASSED (pytest) |
| **Average Query Latency** | ~450ms (Retrieval + Rerank) |

## 🏗️ Technical Architecture Highlights

1. **Two-Stage Retrieval (Reranking):** Initial top-N semantic candidates retrieved via ChromaDB vector cosine distance, followed by precise Cross-Encoder re-ranking for maximum context relevancy.
2. **SHA-256 Document Hashing:** Tracks document changes to allow incremental indexing without full database re-embedding.
3. **Enterprise Logging:** Structured logs saved in logs/app.log with INFO, WARNING, and ERROR trace levels.
4. **Security & Guardrails:** Prompt injection shielding, strict 45s execution timeout, and context insufficiency detection.
5. **Containerized Setup:** Fully Dockerized stack managed via Dockerfile and docker-compose.yml.

## 🚀 Quick Start (Docker)

docker compose up --build

## 🧪 Running Unit Tests

pytest tests/ -v
