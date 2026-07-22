Markdown# 🛸 AeroGrid AI — Enterprise Renewable Energy Maintenance RAG Engine

AeroGrid AI is a production-oriented, containerized **Retrieval-Augmented Generation (RAG)** system designed to assist renewable energy field technicians with wind turbine and solar panel maintenance workflows.

The system combines semantic retrieval, neural reranking, local LLM generation, and enterprise-grade reliability mechanisms to provide accurate, grounded maintenance assistance from technical documentation.

---

## 🚀 Key Features

* 🔎 **Two-Stage Retrieval Pipeline:** Semantic retrieval using ChromaDB vector search + Cross-Encoder reranking for maximum context relevance.
* 📚 **Incremental Document Ingestion:** SHA-256 based document fingerprinting detects new or modified documents and avoids unnecessary re-embedding.
* 🧠 **Local LLM Generation:** Powered by Ollama local inference to support privacy-focused, offline-capable deployments.
* 🛡️ **Security Guardrails:** Prompt injection protection, strict context grounding, and hallucination prevention through `INSUFFICIENT_CONTEXT` fallback.
* ⚡ **Production-Oriented Reliability:** Persistent vector storage, lazy model initialization, structured logging, timeout and exception handling.
* 🐳 **Containerized Deployment:** Fully Dockerized environment for reproducible setup with Docker Compose.

---

## 📊 Evaluation & Benchmark Results

| Metric | Result |
| :--- | :--- |
| **Evaluation Dataset** | 15 Synthetic Field Maintenance Protocols & Safety Documents |
| **Embedding Model** | `sentence-transformers/all-MiniLM-L6-v2` |
| **Reranker Model** | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| **LLM Engine** | Ollama (`llama3.2` Local LLM) |
| **Retrieval Metric** | Precision@3 |
| **Retrieval Precision@3** | **100.00%** |
| **Unit Tests** | **5/5 PASSED** |
| **Average Query Latency** | ~450ms (Retrieval + Reranking) |

---

## 🏗️ System Architecture

```mermaid
graph TD
    %% User & Security Ingestion
    User([User / Client]) -->|1. Submit Query| Guardrail[Prompt Injection Guardrail]

    subgraph Security_Layer [Security & Validation]
        Guardrail -->|Safe Query| Pipeline[RAG Orchestrator]
        Guardrail -->|Injection Detected| Block[Reject Query and Log Event]
    end

    %% Ingestion Pipeline
    subgraph Ingestion_Pipeline [Incremental Indexing SHA-256]
        Docs[Technical Manuals and FAQs] -->|Hash Check| SHA256{Document Changed?}
        SHA256 -->|Yes| Chunking[Text Chunking]
        SHA256 -->|No| Skip[Skip Ingestion]
        Chunking --> Embeddings[Bi Encoder Embeddings]
        Embeddings --> Store[(ChromaDB Vector Store)]
    end

    %% Retrieval Pipeline
    subgraph Retrieval_Pipeline [Two Stage Retrieval Engine]
        Pipeline -->|Vector Search| Store
        Store -->|Candidate Chunks| BiEncoder[Semantic Retrieval]
        BiEncoder -->|Context Candidates| CrossEncoder[Cross Encoder Reranker]
        CrossEncoder -->|MS MARCO MiniLM| ReRanked[Top Ranked Chunks]
    end

    %% Generation
    subgraph Inference_Engine [Local LLM Inference]
        ReRanked -->|Grounded Context| LLM[Local LLM Ollama]
        LLM -->|Generated Answer| Pipeline
    end

    Pipeline -->|Response with Citations| User
🔍 Two-Stage Retrieval Pipeline ArchitectureAeroGrid AI uses a multi-stage retrieval architecture to guarantee precision and context relevancy:Stage 1 — Semantic Search (Bi-Encoder): Documents are transformed into vector embeddings using sentence-transformers/all-MiniLM-L6-v2. The system retrieves candidate document chunks from ChromaDB using cosine similarity search.Stage 2 — Neural Reranking (Cross-Encoder): Retrieved candidates are refined using cross-encoder/ms-marco-MiniLM-L-6-v2. This evaluates direct query-document relationships to eliminate noise and position the top-3 most relevant passages at the top.Stage 3 — Grounded Response Generation: The reranked passages are injected into the local LLM runtime (Ollama) with strict context grounding and citation tracing.🗂️ Project ArchitecturePlaintextAeroGrid_AI/
├── app/
│   ├── ingestion/     # Document processing & SHA-256 incremental indexing
│   ├── retrieval/     # Vector search & Cross-Encoder reranking
│   ├── generation/    # Ollama LLM response generation
│   └── security/      # Prompt injection guardrails & validation
├── documents/         # Maintenance protocols & safety guidelines
├── tests/             # Automated Pytest suite
├── logs/              # Structured application logs (app.log)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
🛡️ Security & Reliability DesignPrompt Injection DefenseThe system applies strict system-level instructions to prevent malicious requests or instruction overrides.PlaintextOnly answer using retrieved maintenance context.

If sufficient information is unavailable:
return INSUFFICIENT_CONTEXT.
Timeout & Exception HandlingOllama inference requests are protected with:45-second execution timeoutNetwork exception handlingDetailed error trace loggingEnterprise LoggingApplication events are tracked through structured logs saved in logs/app.log (INFO, WARNING, ERROR).🧪 TestingRun the automated test suite covering vector retrieval, incremental indexing, SHA-256 change detection, and guardrails:Bashpytest tests/ -v
Validated Components:✅ Vector retrieval & similarity search✅ Incremental document indexing✅ SHA-256 change detection✅ Prompt injection handling✅ Context validation🚀 Quick Start (Docker)Clone the repository and start the application:Bashgit clone [https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git](https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git)
cd AeroGrid_AI
docker compose up --build
💡 Example Use CaseTechnician QueryPlaintextHow should I inspect overheating problems in a wind turbine gearbox?
AeroGrid AI ResponsePlaintextAccording to the maintenance protocol:

1. Check gearbox temperature sensors.
2. Inspect lubrication levels.
3. Perform vibration analysis.

Source:
Wind Turbine Maintenance Protocol #03
📈 Future ImprovementsREST API layer implementation using FastAPIAuthentication and Role-Based Access Control (RBAC)Cloud deployment support (AWS / GCP)Advanced evaluation framework (Recall@K, MRR, Faithfulness metrics)Real-time sensor data integrationInteractive monitoring dashboard👩‍💻 Technical StackComponentTechnologyLanguagePython 3.11+Vector DatabaseChromaDBEmbeddingsSentence Transformers (all-MiniLM-L6-v2)RerankerCross Encoder (ms-marco-MiniLM-L-6-v2)LLM RuntimeOllama (llama3.2)TestingPytestDeploymentDocker & Docker ComposeLoggingStructured Application Logging📌 Project SummaryAeroGrid AI demonstrates a complete RAG engineering workflow including document ingestion, incremental indexing, vector retrieval, neural reranking, local LLM generation, security guardrails, automated evaluation, and containerized deployment.
