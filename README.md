# 🛸 AeroGrid AI
## Enterprise Renewable Energy Maintenance RAG Platform

![CI](https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI/actions/workflows/ci.yml/badge.svg)

AeroGrid AI is an enterprise-oriented Retrieval-Augmented Generation (RAG) platform designed for renewable energy maintenance operations.

The system assists wind turbine and solar field technicians by retrieving verified technical knowledge from maintenance documentation and generating grounded AI responses using local Large Language Models.

AeroGrid AI combines document intelligence, semantic retrieval, neural reranking, local AI inference, security guardrails, and persistent vector storage to deliver reliable AI assistance for industrial maintenance workflows.

---

# 🚀 Key Capabilities

## 🔎 Advanced Retrieval-Augmented Generation Pipeline

AeroGrid AI implements a two-stage retrieval architecture:

### 1. Semantic Retrieval

Maintenance documents are transformed into vector embeddings using:


sentence-transformers/all-MiniLM-L6-v2


Relevant technical knowledge is retrieved from a persistent ChromaDB vector database.

### 2. Neural Reranking

Retrieved candidates are refined using:


cross-encoder/ms-marco-MiniLM-L6-v2


The reranking layer improves:

- Context relevance
- Retrieval precision
- Answer quality

---

# 🏭 Industrial Use Case

Renewable energy technicians operate with large volumes of technical documentation:

- Equipment manuals
- Fault code descriptions
- Safety procedures
- Inspection protocols
- Maintenance instructions

Finding the correct procedure during field operations can be time-consuming.

AeroGrid AI provides:

✅ Fast technical knowledge retrieval  
✅ Documentation-grounded responses  
✅ Source traceability  
✅ Reduced hallucination risk  
✅ Privacy-focused local deployment  

---

# 🏗️ System Architecture


Technician Query

    |
    v

FastAPI Backend

    |
    v

Security Guardrails

    |
    v

Embedding Model

(all-MiniLM-L6-v2)

    |
    v

ChromaDB Vector Database

    |
    v

Semantic Retrieval

    |
    v

Cross Encoder Reranking

    |
    v

Context Assembly

    |
    v

Local LLM Generation

(Ollama + Phi-3)

    |
    v

Grounded Maintenance Response


---

# 🧠 Local AI Generation

AeroGrid AI uses:


Ollama + Phi-3


Advantages:

- Local inference
- Data privacy
- No external API dependency
- Offline-capable architecture
- Industrial deployment compatibility

---

# 🛡️ Security & Reliability

## Prompt Injection Protection

The system validates user input before generation.

Generation policy:


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
✅ Context validation  
✅ Source attribution  

---

# 🔌 API Interface

## Health Check

Endpoint:


GET /health


Example:

```json
{
  "status": "healthy",
  "service": "AeroGrid AI"
}
Maintenance Query

Endpoint:

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

Validated Scenario:

E-301 Generator Overheating Fault

Results:

✅ Correct maintenance procedure retrieved
✅ Safety warnings included
✅ Corrective actions generated
✅ Source documents returned

Pipeline:

Semantic Retrieval
        +
Neural Reranking
        +
Local LLM Generation
🗂️ Project Structure
AeroGrid_AI/

├── src/
│
├── api/
│   └── FastAPI backend
│
├── retrieval/
│   └── ChromaDB retrieval pipeline
│
├── generation/
│   └── Local LLM integration
│
├── security/
│   └── Safety guardrails
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

Swagger documentation:

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
💡 Engineering Decisions
Why RAG?

RAG architecture grounds AI responses in verified technical documentation and reduces hallucination risk.

Why ChromaDB?
Persistent local storage
Lightweight deployment
Suitable for industrial environments
Why Neural Reranking?

Vector retrieval provides speed.

Cross Encoder reranking improves precision and context quality.

Why Local LLM?

Local inference provides:

Data privacy
Operational control
Offline capability
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

AeroGrid AI demonstrates an enterprise-grade RAG architecture for renewable energy maintenance operations.

The project combines:

Document intelligence
Vector search
Neural reranking
Local AI inference
Security controls
API deployment

to deliver reliable AI assistance for industrial maintenance teams.
