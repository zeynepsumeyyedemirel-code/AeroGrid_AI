![CI](https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI/actions/workflows/ci.yml/badge.svg)

# ⚡ AeroGrid AI — Offline Field Service Assistant

<p align="center">
  <img src="https://raw.githubusercontent.com/zeynepsumeyyedemirel-code/AeroGrid_AI/main/screenshots/aerogrid-dashboard-demo.png" width="800">
</p>

AeroGrid AI is an enterprise-oriented **offline Retrieval-Augmented Generation (RAG) assistant** designed for renewable energy field maintenance operations.

## ⚡ Quick Start

### Requirements

- Python 3.11+
- Docker Desktop
- Ollama

### Run

```bash
git clone https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git

cd AeroGrid_AI

docker compose up --build
```

The system helps wind turbine and solar technicians retrieve verified maintenance knowledge and generate **source-grounded AI guidance** using local Large Language Models.

AeroGrid AI combines:

- Document intelligence
- Semantic vector retrieval
- Neural reranking
- Local LLM inference
- Security guardrails
- Source-grounded generation
- Persistent vector storage
- Containerized deployment

to provide reliable AI assistance for industrial maintenance workflows.

---

# 🚀 Key Capabilities

## 🔎 Advanced RAG Pipeline

AeroGrid AI implements a two-stage Retrieval-Augmented Generation architecture.

### 1. Semantic Retrieval

Maintenance documents are converted into embeddings using:


sentence-transformers/all-MiniLM-L6-v2


Stored knowledge is retrieved from:


ChromaDB Persistent Vector Database


### 2. Neural Reranking

Retrieved candidates are refined using:


cross-encoder/ms-marco-MiniLM-L6-v2


Benefits:

- Higher relevance
- Improved context quality
- Reduced hallucination risk

---
# 🏭 Industrial Problem

Renewable energy field technicians work with large amounts of technical information, including equipment manuals, fault code documents, safety procedures, inspection protocols, and maintenance instructions.

During field operations, finding the correct procedure quickly can be slow and error-prone. Traditional AI assistants may generate generic answers without access to verified operational documentation.

AeroGrid AI addresses this challenge by combining Retrieval-Augmented Generation (RAG) with local LLM inference to provide grounded technical assistance for wind turbine and solar panel maintenance scenarios.

The system retrieves relevant information from a local knowledge base before generating responses, enabling:

✅ Faster troubleshooting  
✅ Offline AI assistance  
✅ Documentation-grounded answers  
✅ Source traceability  
✅ Reduced hallucination risk  
✅ Privacy-focused deployment  

## 💡 Key Idea

Keep renewable energy maintenance knowledge local, retrieve only verified technical information, and generate reliable AI assistance without external cloud dependency. 

---

# 🏗️ System Architecture

AeroGrid AI follows a local-first Retrieval-Augmented Generation (RAG) architecture designed for offline renewable energy field operations.

```text
Maintenance Documents
        |
        v
Document Ingestion Pipeline
        |
        v
Embedding Generation
        |
        v
ChromaDB Vector Store
        |
        v
Technician Question
        |
        v
Query Embedding
        |
        v
Semantic Retrieval
        |
        v
Cross Encoder Reranking
        |
        v
Context Validation
        |
        v
Local LLM Inference
(Phi-3 + Ollama / Foundry Local compatible)
        |
        v
Grounded Maintenance Response
```

## Architecture Layers

- **Document Layer:** Processes maintenance manuals, fault codes, and safety procedures.
- **Retrieval Layer:** Uses ChromaDB semantic search with neural reranking.
- **Validation Layer:** Applies grounding rules and safety guardrails.
- **Generation Layer:** Produces responses using local LLM inference.
- **Deployment Layer:** Supports offline enterprise field environments.

---

# 🧠 Local AI Generation

AeroGrid AI follows a local-first AI architecture aligned with Microsoft Foundry Local principles.

The system uses:

- **Model:** Phi-3
- **Local Runtime:** Ollama
- **Architecture:** Local-first RAG architecture aligned with Microsoft Foundry Local principles

Advantages:

- Offline inference
- No external API dependency
- Data privacy
- Local document processing
- Enterprise edge deployment compatibility

This architecture enables secure AI assistance for renewable energy field technicians by keeping operational knowledge and inference workflows locally controlled.

---

# 🛡️ Safety & Reliability

AeroGrid AI follows strict generation rules:


Only answer using retrieved documentation.

If information is missing:
return INSUFFICIENT_CONTEXT.


Implemented protections:

✅ Prompt injection protection  
✅ Context validation  
✅ Source citation  
✅ Persistent vector storage  
✅ Structured logging  
✅ Exception handling  
✅ Timeout management  

---

# 📊 Evaluation & Benchmark Metrics

Current validation scenario:

**Wind Turbine Fault Code E-301**  
**Generator Overheating Fault**

| Metric | Result |
|---|---|
| Evaluation Dataset | 15+ Synthetic Industrial Maintenance Protocols (Wind Turbine Faults, Solar Troubleshooting, Safety Procedures) |
| Retrieval Precision@3 | 100% |
| Unit Tests | 6/6 Passed |
| Average Query Latency | ~450ms |
| Embedding Model | sentence-transformers/all-MiniLM-L6-v2 |
| Reranker Model | cross-encoder/ms-marco-MiniLM-L6-v2 |
| Vector Database | ChromaDB Persistent Storage |
| LLM Runtime | Ollama + Phi-3 Local Inference | 

---

## ✅ Validation Results

Latest local validation run:

```bash
pytest

Result:

6 passed, 1 warning in 16.34s

Validated components:

Retrieval evaluation pipeline
Core configuration tests
RAG system components
Local execution environment 

# 💬 Example Queries

Example maintenance questions:

- What is the corrective action for E-301 generator overheating fault?
- What safety steps are required before turbine maintenance?
- How should an inverter overtemperature issue be handled?
- What are the LOTO requirements for field intervention?

# 🖥️ Dashboard Demo

![AeroGrid AI Dashboard](https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI/blob/main/screenshots/aerogrid-dashboard-demo.png)

AeroGrid AI provides an offline technician assistant interface for renewable energy field operations.

Technicians can submit maintenance questions, retrieve relevant documentation context, and receive grounded AI responses generated from the local knowledge base.

The dashboard demonstrates:
- Offline question answering
- Documentation-grounded maintenance guidance
- Retrieved source context visibility
- Local LLM inference with no cloud dependency

---

# 🗂️ Project Structure

```text
AeroGrid_AI/

├── src/
│   ├── api/
│   │   └── Backend API services
│   │
│   ├── core/
│   │   └── Configuration and shared utilities
│   │
│   ├── ingestion/
│   │   └── Document processing and indexing pipeline
│   │
│   ├── retrieval/
│   │   └── ChromaDB retrieval and reranking pipeline
│   │
│   ├── generation/
│   │   └── Local LLM generation layer
│   │
│   ├── security/
│   │   └── Prompt injection protection and validation
│   │
│   └── evaluation/
│       └── RAG evaluation framework
│
├── docs/
│   ├── wind_turbine/
│   ├── solar_panel/
│   └── safety/
│
├── chroma_db/
│   └── Persistent vector database storage
│
├── screenshots/
│   └── Dashboard demonstrations
│
├── tests/
│   └── Automated validation tests
│
├── dashboard.py
├── app.py
├── retriever.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

```

---

# 🐳 Docker Deployment

AeroGrid AI supports containerized deployment.

Services:

| Service | Purpose |
|---|---|
| Dashboard | Technician interface |
| FastAPI | Backend API |
| ChromaDB | Vector storage |
| Ollama | Local LLM inference |

## Run with Docker

```bash
docker compose up --build
```

---

# 🔌 API

## Health Check

`GET /health`

Example response:

```json
{
  "status": "healthy",
  "service": "AeroGrid AI"
}
```

## Maintenance Query

`POST /query`

Example request:

```json
{
  "question": "What is the corrective action for E-301 generator overheating?"
}
```

Example response:

```json
{
  "answer": "Grounded maintenance response",
  "sources": [
    "wind_turbine_maintenance.txt"
  ]
}
```

---

# 🧰 Technology Stack

| Component | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI |
| Dashboard | Streamlit |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Reranking | Cross Encoder |
| LLM Runtime | Ollama |
| Model | Phi-3 |
| Testing | Pytest |
| Deployment | Docker |

---

# 🚀 Enterprise Design Principles

## Reliability

- Grounded generation
- Source attribution
- Context validation

## Security

- Local inference
- Prompt injection protection
- Privacy-first architecture

## Scalability

- Modular components
- Persistent storage
- Container deployment

## Maintainability

- Automated testing
- Structured logging
- Clean architecture

---

# 🔮 Future Roadmap

## Phase 1 — Core RAG

- ✅ Retrieval pipeline
- ✅ Local LLM generation
- ✅ Security layer

## Phase 2 — Enterprise Platform

- Authentication
- Role-based technician access
- Monitoring dashboard
- Cloud deployment

## Phase 3 — Industrial Intelligence

- Sensor integration
- Predictive maintenance
- Anomaly detection

---

# 👩‍💻 Project Summary

AeroGrid AI demonstrates an enterprise-grade offline Retrieval-Augmented Generation (RAG) architecture for renewable energy maintenance.

The project combines:

- Retrieval-Augmented Generation (RAG)
- Semantic vector search
- Neural reranking
- Local AI inference
- Safety controls
- Containerized deployment

to deliver reliable AI assistance for industrial field service operations.

---

# ⚠️ Limitations

- The assistant provides guidance only from available local documentation.
- Missing documentation may result in INSUFFICIENT_CONTEXT responses.
- High-risk procedures should always be verified against official manuals and site safety protocols.
