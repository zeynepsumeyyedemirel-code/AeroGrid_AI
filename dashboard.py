import streamlit as st
import time
from app import AeroGridAssistant

st.set_page_config(
    page_title="AeroGrid AI - Field Support",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ AeroGrid AI — Offline Field Service Assistant")
st.caption("🌐 Status: **OFFLINE MODE (Ollama Local LLM + RAG Active)**")

@st.cache_resource
def load_assistant():
    return AeroGridAssistant()

with st.spinner("🧠 Initializing AeroGrid AI Engine & Knowledge Base..."):
    assistant = load_assistant()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("❓ Technician Query")
    
    preset_query = st.selectbox(
        "Select a quick sample issue or write below:",
        [
            "Custom Query...",
            "What should I do if Error Code E-301 occurs on a wind turbine?",
            "What is the maximum wind speed limit for climbing the tower?",
            "How should I perform solar panel cleaning and inspection?"
        ]
    )
    
    if preset_query != "Custom Query...":
        user_input = st.text_area("Field Question:", value=preset_query, height=120)
    else:
        user_input = st.text_area("Field Question:", value="", placeholder="e.g., Explain Fault Code W-102...", height=120)
        
    submit_btn = st.button("🚀 Ask AeroGrid AI", type="primary")

with col2:
    st.subheader("💬 AI Field Guidance")
    if submit_btn and user_input.strip():
        with st.spinner("🔍 Searching docs & generating response..."):
            # RAG Araması ve Yanıt
            response = assistant.ask(user_input)
            
            # Doküman bağlamını göster
            results = assistant.retriever.search(user_input, top_k=2)
            context_str = "\n\n".join([f"📄 [Source: {r['source']}]\n{r['text']}" for r in results])
            
            st.success("Response Generated Successfully!")
            st.info(response)
            
            with st.expander("📂 View Retrieved Technical Docs Context"):
                st.code(context_str, language="markdown")