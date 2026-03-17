import streamlit as st

def render_header():
    st.markdown("""
        <h1 style='text-align:center; color: #2E7D32;'>
            🌍 RAG-Powered Geoscience Assistant
        </h1>
        <p style='text-align:center; color: #666; font-size:16px;'>
            Ask questions grounded in geological literature and research papers.
            Every answer is evidence-linked with source citations.
        </p>
        <hr/>
    """, unsafe_allow_html=True)

def render_source_card(source: dict, index: int):
    st.markdown(
        f"""<div style="
            border-left: 3px solid #2E7D32;
            padding: 8px 12px;
            margin: 4px 0;
            background: rgba(46,125,50,0.05);
            border-radius: 4px;
            font-size: 13px;
        ">
        <b>Source {index+1}:</b> {source['file']} — Page {source['page']}<br>
        <span style="color: #888; font-size: 12px;">
            {source['excerpt']}...
        </span>
        </div>""",
        unsafe_allow_html=True
    )