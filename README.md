# 🛸 AeroGrid AI
## Enterprise Renewable Energy Maintenance RAG Platform

![CI](https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI/actions/workflows/ci.yml/badge.svg)

AeroGrid AI is an enterprise-oriented Retrieval-Augmented Generation (RAG) platform designed for renewable energy maintenance operations.

The system assists wind turbine and solar field technicians by retrieving verified technical knowledge from maintenance documentation and generating grounded AI responses using local Large Language Models.

AeroGrid AI combines:

- Document intelligence
- Semantic retrieval
- Neural reranking
- Local LLM inference
- Security guardrails
- Source-grounded generation
- Persistent vector storage
- FastAPI backend

to deliver reliable AI assistance for industrial maintenance workflows.

---

# 🚀 Key Capabilities

## 🔎 Advanced RAG Pipeline

AeroGrid AI implements a two-stage Retrieval-Augmented Generation architecture.

### 1. Semantic Retrieval

Maintenance documents are transformed into vector embeddings using:

```
sentence-transformers/all-MiniLM-L6-v2
```

Relevant maintenance knowledge is retrieved from a persistent ChromaDB vector database.

### 2. Neural Reranking

Retrieved candidates are refined using:

```
cross-encoder/ms-marco-MiniLM-L6-v2
```

The reranking stage improves:

- Context relevance
- Retrieval precision
- Answer reliability

---

# 🏭 Industrial Problem

Renewable energy technicians work with large volumes of technical documentation:

- Equipment manuals
- Fault code documentation
- Safety procedures
- Inspection protocols
- Maintenance instructions

Finding the correct procedure during field operations can be slow and error-prone.

AeroGrid AI provides:

✅ Faster troubleshooting  
✅ Documentation-grounded answers  
✅ Source traceability  
✅ Reduced hallucination risk  
✅ Privacy-focused deployment  

---

# 🏗️ System Architecture

```
Technician Question

        |
        v

FastAPI Backend

        |
        v

Security Guardrails

        |
        v

Query Embedding

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

Ollama Local LLM

        |
        v

Grounded Maintenance Response
```

---

# 🧠 Local AI Generation

AeroGrid AI uses:

```
Ollama + Phi-3
```

Benefits:

- Local inference
- Data privacy
- No external API dependency
- Offline-capable architecture
- Industrial deployment compatibility

---

# 🛡️ Security & Reliability

## Prompt Injection Protection

The system follows strict generation rules:

```
Only answer using retrieved maintenance context.

If sufficient information is unavailable:
return INSUFFICIENT_CONTEXT.
```

## Reliability Features

Implemented:

✅ Persistent vector storage  
✅ Structured logging  
✅ Exception handling  
✅ Timeout management  
✅ Context validation  
✅ Source attribution  

---

# 🔌 API
## API Documentation

Interactive API documentation is available through FastAPI Swagger UI.

Swagger UI:
http://127.0.0.1:8000/docs

OpenAPI specification:
http://127.0.0.1:8000/openapi.json

---

## Health Check

```
GET /health
```

Example:

```json
{
  "status": "healthy",
  "service": "AeroGrid AI"
}
```

---

## Maintenance Query

```
POST /query
```

Example request:

```json
{
  "question": "What is the corrective action for E-301 generator overheating?"
}
```

Example response:

```json
{
  "answer": "Inspect cooling fan fuses and relays. Check coolant levels.",
  "sources": [
    "wind_turbine_maintenance.txt"
  ]
}
```

---

# 📊 Evaluation Results

Current Knowledge Base:

```
278 indexed maintenance chunks
```

Validated Scenario:

```
E-301 Generator Overheating Fault
```

Results:

✅ Relevant maintenance procedure retrieved  
✅ Safety warnings included  
✅ Corrective actions generated  
✅ Source documents returned  

Pipeline:

```
Semantic Retrieval
        +
Neural Reranking
        +
Local LLM Generation
```

---

# 🗂️ Project Structure

```
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
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone repository:

```bash
git clone https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git

cd AeroGrid_AI
```

Create environment:

```bash
python -m venv AeroGrid_venv

source AeroGrid_venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run API:

```bash
uvicorn src.api.main:app --reload
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

# 🧰 Technology Stack

| Component | Technology |
|---|---|
| Backend | FastAPI |
| Language | Python |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Reranker | Cross Encoder |
| LLM Runtime | Ollama |
| Model | Phi-3 |
| Testing | Pytest |
| Deployment | Docker |

---

# 🎯 Demo Scenario

## Industrial Maintenance Query

A field technician encounters a wind turbine generator overheating fault.

Question:

```
What is the corrective action for E-301 generator overheating?
```

AeroGrid AI retrieves:

- Fault documentation
- Safety procedures
- Corrective maintenance steps

and generates a grounded response with source references.

---

# 🏭 Enterprise Design Principles

## Reliability

- Documentation-grounded generation
- Source attribution
- Context validation

## Security

- Prompt injection protection
- Local inference
- Privacy-focused deployment

## Scalability

- Persistent vector storage
- Modular architecture
- Containerized deployment

## Maintainability

- Automated testing
- Structured logging
- Clear separation of components

---

# 🔮 Future Roadmap

## Phase 1 — Core RAG

✅ Retrieval pipeline  
✅ Local LLM generation  
✅ Security layer  

## Phase 2 — Enterprise Platform

- Authentication
- Role-Based Access Control
- Cloud deployment
- Monitoring dashboard

## Phase 3 — Industrial Intelligence

- Real-time sensor integration
- Predictive maintenance
- Automated anomaly detection

---

# 👩‍💻 Project Summary

AeroGrid AI demonstrates an enterprise-grade RAG architecture for renewable energy maintenance.

The project combines:

- Document intelligence
- Vector search
- Neural reranking
- Local AI inference
- Security controls
- API deployment

to deliver reliable AI assistance for industrial maintenance teams.

---

# 🖥️ Project Demo

## Dashboard Preview

> Screenshot of AeroGrid AI maintenance assistant interface.

<!-- Add dashboard screenshot here -->


## Maintenance Assistant Workflow

AeroGrid AI workflow:

```
Technician Question

        ↓

FastAPI API Request

        ↓

Document Retrieval

        ↓

Semantic Search

        ↓

Neural Reranking

        ↓

Local LLM Generation

        ↓

Grounded Maintenance Answer
```

Example maintenance query:

```
What is the corrective action for E-301 generator overheating?
```

Generated response:

```
Inspect cooling fan fuses and relays.
Check coolant levels.
Verify temperature sensor readings.

Sources:
wind_turbine_maintenance.txt
```

---

# 🐳 Docker Deployment
## Services

Docker Compose manages:

| Service | Purpose |
|---|---|
| FastAPI | Backend API layer |
| ChromaDB | Vector storage |
| Ollama | Local LLM inference |
| RAG Pipeline | Retrieval and generation workflow |

AeroGrid AI supports containerized deployment using Docker Compose.

## Build and Run

Clone repository:

```bash
git clone https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git

cd AeroGrid_AI
```

Start the platform:

```bash
docker compose up --build
```

The system launches:

- FastAPI backend
- RAG pipeline
- Vector database storage
- Local AI inference services

---

## Container Architecture

```
Docker Compose

      |
      |

FastAPI Service

      |
      |

RAG Pipeline

      |
      |

ChromaDB Vector Storage

      |
      |

Ollama Local LLM
```

---

# 🔌 Enterprise API Documentation

## Health Monitoring

### Endpoint

```
GET /health
```

Purpose:

Service availability monitoring.

Response:

```json
{
  "status": "healthy",
  "service": "AeroGrid AI",
  "version": "1.0"
}
```

---

## Maintenance Query API

### Endpoint

```
POST /query
```

Purpose:

Submit a maintenance question and receive a grounded AI response.

Request:

```json
{
  "question": "How should gearbox overheating be inspected?"
}
```

Response:

```json
{
  "answer": "Inspect lubrication system and temperature sensors.",
  "sources": [
    "gearbox_maintenance_manual.pdf"
  ],
  "confidence": "high"
}
```

---

# 📈 Engineering Metrics

Current system capabilities:

| Metric | Value |
|---|---|
| Indexed Knowledge Chunks | 278 |
| Retrieval Method | Semantic Search |
| Reranking | Cross Encoder |
| LLM Runtime | Ollama |
| Deployment | Docker |
| API Framework | FastAPI |
| Testing Framework | Pytest |

---

# 🚀 Production Vision

Future enterprise extensions:

- Authentication and authorization
- Role-based technician access
- Cloud deployment
- Monitoring dashboards
- Real-time sensor integration
- Predictive maintenance models

---

