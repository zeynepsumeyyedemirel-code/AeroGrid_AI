# AeroGrid AI — Offline Field Service Assistant

![AeroGrid AI Dashboard Preview](docs/preview.png)

A zero-latency, fully local AI decision-support tool engineered for renewable energy field technicians (wind & solar) working in off-grid environments with zero cloud access or internet connectivity.

The system processes technical manuals, high-voltage safety SOPs, and fault code databases on-device using local Vector Embeddings and Ollama (Microsoft Phi-3).

---

## System Architecture & RAG Pipeline


┌──────────────────────────┐      ┌──────────────────────────┐
│  Technical Docs (.txt)   │      │   User Query (Field)     │
│  Wind / Solar / Safety   │      │ "E-301 fault code"       │
└────────────┬─────────────┘      └────────────┬─────────────┘
             │                                 │
             ▼                                 ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│ Sentence-Transformers    │      │ Query Vector Encoding    │
│ (all-MiniLM-L6-v2)       │      └────────────┬─────────────┘
└────────────┬─────────────┘                   │
             │                                 │
             ▼                                 ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│ Local Vector Index       ├─────►│ Cosine Similarity Match  │
│ Matrix (In-Memory)       │      │ (Top-K Context Chunks)   │
└──────────────────────────┘      └────────────┬─────────────┘
                                               │
                                               ▼
┌──────────────────────────┐      ┌──────────────────────────┐
│ Safety & Context Guarded ├─────►│ Ollama (Microsoft Phi-3) │
│ System Prompt            │      │ On-Device LLM Inference  │
└──────────────────────────┘      └────────────┬─────────────┘
                                               │
                                               ▼
                                  ┌──────────────────────────┐
                                  │ Field Guidance & Source  │
                                  │ Verification Context UI  │
                                  └──────────────────────────┘
```


---

## Local Setup & Execution

1. **Prerequisites (Ollama & Model):**
   ```bash
   ollama pull phi3
   ```

2. **Clone & Environment Setup:**
   ```bash
   git clone [https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git](https://github.com/zeynepsumeyyedemirel-code/AeroGrid_AI.git)
   cd AeroGrid_AI

   python3 -m venv AeroGrid_venv
   source AeroGrid_venv/bin/activate
   pip install streamlit sentence-transformers torch requests
   ```

3. **Launch Local Field Assistant:**
   ```bash
   streamlit run dashboard.py
   ```

---

## Document Knowledge Base Structure

The local vector engine indexes raw technical documentation located in the `docs/` directory:
* `docs/wind_turbine_maintenance.txt` — E-101 (Pitch Control), E-301 (Stator Overheating), E-404 (Yaw Jam) fault code SOPs and hydraulic limits.
* `docs/solar_panel_maintenance.txt` — F-80 (Grid Overvoltage), F-102 (Ground Fault) troubleshooting, and combiner box inspection steps.
* `docs/field_safety_rules.txt` — LOTO (Lockout/Tagout) 8-step isolation procedures, Arc Flash boundaries, and HV PPE requirements.
