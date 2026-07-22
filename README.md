CTRL + O
Enter
CTRL + X
# 🛸 AeroGrid AI — Enterprise Renewable Energy Maintenance RAG Engine

AeroGrid AI is a production-oriented Retrieval-Augmented Generation (RAG) system designed for renewable energy maintenance operations.

The platform assists wind turbine and solar field technicians by retrieving verified maintenance knowledge and generating grounded AI responses using local LLM inference.

The system combines:

- Semantic document retrieval
- Neural reranking
- Local LLM generation
- Security guardrails
- Source-grounded answers
- Persistent vector storage
- FastAPI backend

to provide reliable AI assistance for industrial maintenance workflows.

---

# 🚀 System Overview

Renewable energy technicians work with large amounts of:

- Equipment manuals
- Fault code documentation
- Safety procedures
- Inspection protocols
- Maintenance instructions

AeroGrid AI reduces troubleshooting time by providing an AI-powered maintenance assistant that:

✅ Retrieves relevant technical knowledge  
✅ Generates documentation-grounded answers  
✅ Provides source traceability  
✅ Reduces hallucination risk  
✅ Supports privacy-focused local deployment  

---

# 🏗️ Architecture


Technician Query
|
v
FastAPI API Layer
|
v
Security Guardrails
|
v
Embedding Model
(all-MiniLM-L6-v2)
|
v
ChromaDB Vector Store
|
v
Semantic Retrieval
|
v
Cross Encoder Reranking
(MS MARCO MiniLM)
|
v
Context Assembly
|
v
Ollama Local LLM
(Phi-3)
|
v
Grounded Maintenance Response


---

# 🔎 RAG Pipeline

## Document Ingestion

Maintenance documents are processed through:

- Document loading
- Text chunking
- Embedding generation
- Vector indexing
- Persistent storage

Vector database:


ChromaDB


---

## Semantic Retrieval

User queries are converted into embeddings using:


sentence-transformers/all-MiniLM-L6-v2


Relevant maintenance chunks are retrieved from the knowledge base.

---

## Neural Reranking

Retrieved candidates are refined using:


cross-encoder/ms-marco-MiniLM-L6-v2


The reranker improves context relevance before generation.

---

## Grounded Generation

The local LLM receives:


User Question
+
Retrieved Maintenance Context
+
Safety Instructions


and generates a documentation-grounded response.

---

# 🧠 Local AI Generation

AeroGrid AI uses:


Ollama + Phi-3


Benefits:

- Local inference
- Data privacy
- No external API dependency
- Offline-capable architecture
- Industrial deployment compatibility

---

# 🛡️ Security & Reliability

## Prompt Injection Protection

The system validates user input before generation.

Policy:


Only answer using retrieved maintenance context.

If sufficient information is unavailable:
return INSUFFICIENT_CONTEXT.


---

## Reliability Features

Implemented:

✅ Persistent vector storage  
✅ Structured logging  
✅ Exception handling  
✅ Timeout management  
✅ Source attribution  
✅ Context validation  

---

# 🔌 API

## Health Check


GET /health


Example:

```json
{
  "status": "healthy",
  "service": "AeroGrid AI"
}
Maintenance Query
POST /query

Request:

{
  "question": "What is the corrective action for E-301 generator overheating?"
}

Response:

{
  "answer": "Inspect cooling fan fuses and relays. Check coolant levels.",
  "sources": [
    "wind_turbine_maintenance.txt"
  ]
}
📊 Evaluation

Current Knowledge Base:

278 indexed maintenance chunks

Pipeline:

Semantic Retrieval
        +
Cross Encoder Reranking
        +
Local LLM Generation

Validated Scenario:

E-301 Generator Overheating Fault

Result:

✅ Relevant maintenance procedure retrieved
✅ Safety warnings included
✅ Corrective actions generated
✅ Source documents returned

🗂️ Project Structure
AeroGrid_AI/

├── src/
│
├── api/
│   └── FastAPI application
│
├── retrieval/
│   └── ChromaDB retrieval pipeline
│
├── generation/
│   └── Local LLM integration
│
├── security/
│   └── Guardrails
│
├── documents/
│   └── Maintenance knowledge base
│
├── tests/
│
├── chroma_db/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
⚙️ Installation

Clone repository:

git clone https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git

cd AeroGrid_AI

Create environment:

python -m venv AeroGrid_venv

source AeroGrid_venv/bin/activate

Install dependencies:

pip install -r requirements.txt

Run API:

uvicorn src.api.main:app --reload

Swagger:

http://127.0.0.1:8000/docs
🧰 Technology Stack
Component	Technology
Backend	FastAPI
Language	Python
Vector Database	ChromaDB
Embeddings	Sentence Transformers
Reranker	Cross Encoder
LLM Runtime	Ollama
Model	Phi-3
Testing	Pytest
Deployment	Docker
🔮 Future Roadmap
Phase 1 — Core RAG

✅ Retrieval pipeline
✅ Local LLM generation
✅ Security layer

Phase 2 — Enterprise Platform
Authentication
Role-Based Access Control
Cloud deployment
Monitoring dashboard
Phase 3 — Industrial Intelligence
Real-time sensor integration
Predictive maintenance
Automated anomaly detection
👩‍💻 Project Summary

AeroGrid AI demonstrates an enterprise-oriented RAG architecture for renewable energy maintenance.

The project combines:

Document intelligence
Vector search
Neural reranking
Local AI inference
Security controls
API deployment

to deliver reliable AI assistance for industrial maintenance teams.
