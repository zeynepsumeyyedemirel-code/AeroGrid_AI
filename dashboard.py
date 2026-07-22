import streamlit as st
import requests
import os
from retriever import retrieve_context, build_vector_store, DOCS_DIR

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "phi3"

st.set_page_config(
    page_title="AeroGrid AI — Offline Field Service Assistant",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ AeroGrid AI — Offline Field Service Assistant")
st.caption("🌐 Status: OFFLINE MODE (Ollama Local LLM + ChromaDB Vector Store Active)")

# Sidebar for Dynamic File Upload (PDF / TXT)
with st.sidebar:
    st.header("📂 Document Management")
    st.markdown("Upload new manuals or SOPs directly into ChromaDB.")
    
    uploaded_files = st.file_uploader(
        "Upload PDF or TXT manuals:",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )
    
    if st.button("📥 Index Uploaded Documents", type="secondary"):
        if uploaded_files:
            for file in uploaded_files:
                save_path = os.path.join(DOCS_DIR, file.name)
                with open(save_path, "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"Saved {len(uploaded_files)} file(s). Re-indexing ChromaDB...")
            build_vector_store()
            st.rerun()
        else:
            st.warning("Please select at least one file to upload.")

# Main Interface
QUICK_ISSUES = {
    "Custom Query...": "",
    "Fault Code E-301: Stator Overheating": "What is the SOP for fault code E-301?",
    "Fault Code F-80: Grid Overvoltage": "How do I resolve grid overvoltage F-80?",
    "Safety Protocol: LOTO 8-Step Procedure": "Explain the 8-step LOTO procedure.",
    "Safety Protocol: Fall Protection & Height Rules": "What is the maximum wind speed limit for climbing towers?"
}

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("❓ Technician Query")
    selected_preset = st.selectbox("Select a quick sample issue or write below:", list(QUICK_ISSUES.keys()))
    
    default_text = QUICK_ISSUES[selected_preset] if selected_preset != "Custom Query..." else ""
    user_query = st.text_area("Field Question:", value=default_text, height=120, placeholder="e.g. How to handle stator overheating on E-301?")
    
    submit_btn = st.button("🚀 Ask AeroGrid AI", type="primary")

with col2:
    st.subheader("💬 AI Field Guidance")
    
    if submit_btn and user_query.strip():
        with st.spinner("Retrieving ChromaDB contexts and generating guidance..."):
            retrieved_matches = retrieve_context(user_query, top_k=3)
            
            context_str = "\n\n".join([f"Source: {m['source']} (Relevance: {m['score']}%)\n{m['content']}" for m in retrieved_matches])
            
            system_prompt = f"""
You are AeroGrid AI, an offline field service assistant for renewable energy engineers.
Your duty is to provide precise, safety-critical troubleshooting guidance based STRICTLY on the provided official documents.

CRITICAL INSTRUCTIONS:
- Base your instructions ONLY on the provided context.
- If high-voltage, height safety, or LOTO procedures are involved, emphasize safety equipment and isolation steps first.
- Always cite the document source (e.g., Source: wind_turbine/E-301.txt) mentioned in the context.
- If the context does not contain enough information, state clearly that official documentation must be consulted.

DOCUMENTATION CONTEXT:
{context_str}

USER QUESTION:
{user_query}

ANSWER:
"""
            
            payload = {
                "model": MODEL_NAME,
                "prompt": system_prompt,
                "stream": False
            }
            
            try:
                response = requests.post(OLLAMA_URL, json=payload, timeout=60)
                if response.status_code == 200:
                    result_json = response.json()
                    answer = result_json.get("response", "No response generated.")
                    
                    st.success("Response Generated Successfully!")
                    st.markdown(answer)
                    
                    st.warning("⚠️ **SAFETY DISCLAIMER:** This guidance is generated offline via AeroGrid RAG. Always verify high-voltage and height procedures against physical manual placards on site before taking action.")
                    
                    # Context expander with Score Visualizations
                    with st.expander("🔍 View Retrieved ChromaDB Contexts & Match Scores"):
                        for idx, match in enumerate(retrieved_matches, 1):
                            st.markdown(f"**Chunk {idx}:** `{match['source']}` — **Match Score: `{match['score']}%`**")
                            st.code(match['content'], language="text")
                            st.divider()
                else:
                    st.error(f"Ollama API returned status code {response.status_code}.")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to local Ollama server: {e}")
                st.info("Make sure Ollama is running locally via `ollama serve` and `phi3` model is available.")
