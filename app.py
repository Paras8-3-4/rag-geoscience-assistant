import streamlit as st
import httpx
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'frontend'))

from components import render_header, render_source_card

API_URL = "https://rag-geoscience-assistant.onrender.com"
MAX_FILES = 10
MAX_SIZE_MB = 150
ALLOWED_TYPES = ["pdf", "txt", "docx", "xlsx", "xls"]

st.set_page_config(
    page_title="GeoScience RAG Assistant",
    page_icon="🌍",
    layout="wide"
)

render_header()

with st.sidebar:
    st.markdown("### 📂 Upload Documents")
    st.caption(f"Max {MAX_FILES} files · Max {MAX_SIZE_MB}MB total · PDF, DOCX, TXT, XLSX")

    uploaded_files = st.file_uploader(
        "Choose files",
        type=ALLOWED_TYPES,
        accept_multiple_files=True,
        help=f"Upload up to {MAX_FILES} files, total size under {MAX_SIZE_MB}MB"
    )

    if uploaded_files:
        total_mb = sum(f.size for f in uploaded_files) / (1024 * 1024)
        st.caption(f"{len(uploaded_files)} file(s) selected · {total_mb:.1f}MB total")

        for f in uploaded_files:
            size_kb = f.size / 1024
            st.markdown(f"📄 `{f.name}` — {size_kb:.0f}KB")

        col1, col2 = st.columns(2)
        with col1:
            process_btn = st.button("⚡ Process Files", type="primary", use_container_width=True)
        with col2:
            clear_btn = st.button("🗑️ Reset Index", use_container_width=True)

        if process_btn:
            if len(uploaded_files) > MAX_FILES:
                st.error(f"Too many files. Max {MAX_FILES} allowed.")
            elif total_mb > MAX_SIZE_MB:
                st.error(f"Total size {total_mb:.1f}MB exceeds {MAX_SIZE_MB}MB limit.")
            else:
                with st.spinner(f"Processing {len(uploaded_files)} file(s)..."):
                    try:
                        files_data = [
                            ("files", (f.name, f.getvalue(),
                             "application/octet-stream"))
                            for f in uploaded_files
                        ]
                        response = httpx.post(
                            f"{API_URL}/upload",
                            files=files_data,
                            timeout=120.0
                        )
                        result = response.json()

                        if response.status_code == 200:
                            st.success(
                                f"✅ {result['files_processed']} file(s) processed · "
                                f"{result['chunks_added']} chunks indexed"
                            )
                            if result["errors"]:
                                for err in result["errors"]:
                                    st.warning(f"⚠️ {err}")
                        else:
                            st.error(f"Upload failed: {result.get('detail', 'Unknown error')}")

                    except httpx.ConnectError:
                        st.error("Cannot connect to backend. Is the server running?")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

        if clear_btn:
            with st.spinner("Clearing index..."):
                try:
                    response = httpx.delete(f"{API_URL}/reset", timeout=30.0)
                    if response.status_code == 200:
                        st.success("✅ Index cleared. Upload new documents to start.")
                        st.session_state.messages = []
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    show_sources = st.toggle("Show source documents", value=True)
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.info(
        "Upload your geoscience documents and ask questions. "
        "Every answer is grounded in your uploaded files with source citations."
    )
    st.markdown("**Model:** Llama 3.3 70B via Groq")
    st.markdown("**Embeddings:** all-MiniLM-L6-v2")
    st.markdown("**Vector DB:** FAISS")

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
        <div style='text-align:center; padding:60px 20px; color:#888;'>
            <h3>👆 Upload documents in the sidebar to get started</h3>
            <p style='margin-top:12px;'>Then ask questions like:</p>
            <p><i>"What are the applications of RAG in geoscience?"</i></p>
            <p><i>"Explain the retriever module architecture"</i></p>
            <p><i>"What are the future research directions?"</i></p>
        </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if show_sources and msg.get("sources"):
            with st.expander(f"📄 {len(msg['sources'])} source(s) retrieved"):
                for i, src in enumerate(msg["sources"]):
                    render_source_card(src, i)

if prompt := st.chat_input("Ask about your uploaded documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                response = httpx.post(
                    f"{API_URL}/query",
                    json={"question": prompt},
                    timeout=60.0
                )
                data = response.json()
                answer = data.get("answer", "")
                sources = data.get("sources", [])

                if not answer.strip():
                    answer = "I could not find a relevant answer in the uploaded documents."

                st.write(answer)

                if show_sources and sources:
                    with st.expander(f"📄 {len(sources)} source(s) retrieved"):
                        for i, src in enumerate(sources):
                            render_source_card(src, i)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources
                })

            except httpx.ConnectError:
                st.error("Cannot connect to backend.")
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")