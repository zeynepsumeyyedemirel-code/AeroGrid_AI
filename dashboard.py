import streamlit as st
import requests
import os
import logging
from retriever import retrieve_context, build_vector_store, DOCS_DIR, LOG_FILE

logger = logging.getLogger("AeroGrid_Dashboard")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434/api/generate"
)

MODEL_NAME = "phi3"
REQUEST_TIMEOUT = 45 # seconds

st.set_page_config(
    page_title="AeroGrid AI — Offline Field Service Assistant",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ AeroGrid AI — Offline Field Service Assistant")
st.caption("🌐 Status: OFFLINE MODE (Ollama Local LLM + ChromaDB Vector Store Active)")

# Sidebar for Dynamic File Upload (PDF / TXT) & Logs
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
            logger.info(f"Saved {len(uploaded_files)} file(s) from UI upload.")
            st.success(f"Saved {len(uploaded_files)} file(s). Running incremental indexing...")
            build_vector_store(force_reindex=False)
            st.rerun()
        else:
            st.warning("Please select at least one file to upload.")
            
    st.divider()
    st.header("📋 System Logs")
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as lf:
            log_lines = lf.readlines()[-20:] # Show last 20 log entries
            st.text_area("Recent App Logs:", value="".join(log_lines), height=180)

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

    selected_preset = st.selectbox(
        "Select a quick sample issue or write below:",
        list(QUICK_ISSUES.keys())
    )
    if "user_query" not in st.session_state:
        st.session_state.user_query = ""

    if selected_preset != "Custom Query...":
        if st.session_state.get("last_selected_preset") != selected_preset:
            st.session_state.user_query = QUICK_ISSUES[selected_preset]
            st.session_state.last_selected_preset = selected_preset

    user_query = st.text_area(
        "Field Question:",
        key="user_query",
        height=120,
        placeholder="e.g. How to handle stator overheating on E-301?"
    )

    submit_btn = st.button("🚀 Ask AeroGrid AI", type="primary")

with col2:
    st.subheader("💬 AI Field Guidance")
    
    if submit_btn and user_query.strip():
        logger.info(f"User submitted query: '{user_query}'")
        with st.spinner("Retrieving ChromaDB contexts and generating guidance..."):
            retrieved_matches = retrieve_context(user_query, top_k=3)
            
            context_str = "\n\n".join([
                f"Source: {m['source']} (Page: {m['page']})\n{m['content']}"
                for m in retrieved_matches
            ])
            
            system_prompt = f"""
You are AeroGrid AI, an offline technical maintenance assistant for renewable energy field technicians.

IMPORTANT:
- Answer ONLY using the provided documentation context.
- Do not use outside knowledge.
- Never mention match scores, similarity scores, chunks, or retrieval metadata.
- Never mention the retrieval process.
- Use documented corrective actions and troubleshooting information when available.
- Do not invent procedures or add information that is not present in the documentation.
- Only return INSUFFICIENT_CONTEXT when the documentation contains no relevant information for the technician question.
- Always cite source document name and page number.

DOCUMENTATION CONTEXT:
{context_str}

TECHNICIAN QUESTION:
{user_query}

Answer format rules:
- Start directly with the answer.
- Never mention match scores, similarity scores, chunks, or retrieval metadata.
- Never describe the retrieval process.
- Use only information available in the documentation context.
- If the documentation provides corrective actions, summarize them clearly.
- Do not invent procedures or add technical details that are not present in the documentation.
- If the documentation contains partial information, explain the available information and advise verification with official manuals when necessary.
- Only return INSUFFICIENT_CONTEXT when no relevant documentation exists for the technician question.
- Always cite the exact source filename and page number.
"""

            
            payload = {
                "model": MODEL_NAME,
                "prompt": system_prompt,
                "stream": False
            }
            
            try:
                response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
                
                if response.status_code == 200:
                    result_json = response.json()
                    answer = result_json.get("response", "No response generated.")
                    
                    st.success("Response Generated Successfully!")
                    st.markdown(answer)
                    
                    st.warning("⚠️ **SAFETY DISCLAIMER:** Guidance generated offline via AeroGrid RAG. Always verify high-voltage/height SOPs against physical manual placards on site.")
                    
                    with st.expander("🔍 View Retrieved Contexts & Metadata"):
                        for idx, match in enumerate(retrieved_matches, 1):
                            st.markdown(f"**Chunk {idx}:** `{match['source']}` (Page {match['page']}) — **Match Score: `{match['score']}%`**")
                            st.code(match['content'], language="text")
                            st.divider()
                else:
                    logger.error(f"Ollama returned HTTP error status: {response.status_code}")
                    st.error(f"Ollama Service Error (Code {response.status_code}): Unable to complete request.")
                    
            except requests.exceptions.Timeout:
                logger.error("Ollama API request timed out.")
                st.error(f"⏱️ Request Timeout: Ollama local LLM did not respond within {REQUEST_TIMEOUT} seconds.")
            except requests.exceptions.ConnectionError:
                logger.error("Failed to connect to Ollama server.")
                st.error("🔌 Connection Refused: Unable to reach local Ollama server at http://host.docker.internal:11434.")
                st.info("Ensure Ollama is running in the background via `ollama serve`.")
            except requests.exceptions.RequestException as e:
                logger.error(f"Unexpected request exception: {e}")
                st.error(f"Unexpected API error: {e}")
