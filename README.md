# AeroGrid AI — Offline Field Service Assistant

![AeroGrid AI Dashboard Preview](docs/preview.png)

A zero-latency, fully local AI decision support tool engineered for renewable energy field technicians (wind & solar) working in off-grid environments with no internet connectivity.

The system processes technical manuals, high-voltage safety SOPs, and fault code databases on-device using local Vector Embeddings and Ollama (Microsoft Phi-3).

## Engineering Approach & Core Mechanics

Standard cloud-based LLM architectures fail in remote field operations due to network dependency and potential data privacy risks. AeroGrid AI addresses this via:
* **Edge-Native Architecture:** The embedding pipeline, vector search, and LLM inference run 100% locally on the host machine.
* **Semantic Vector Retrieval (RAG):** Replaces traditional keyword/TF-IDF matching with `Sentence-Transformers` (`all-MiniLM-L6-v2`) to capture technical domain context accurately.
* **Source Transparency & Auditability:** Exposes retrieved context fragments ("View Retrieved Technical Docs Context") in the UI to prevent LLM hallucinations during safety-critical procedures.

## Tech Stack

* **LLM Engine:** Microsoft Phi-3 (via Ollama Runtime)
* **Embedding Model:** `sentence-transformers/all-MiniLM-L6-v2`
* **Frontend / UX:** Streamlit
* **Core Language:** Python 3.10+
* **Vector Store:** Custom Cosine Similarity Matrix Pipeline

## Local Setup & Execution

1. **Prerequisites (Ollama & Model):**
   ```bash
   ollama pull phi3
