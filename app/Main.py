from pathlib import Path
import sys

# Ensure repo root is on Python path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
from app.utils.session_state import init_session_state
from app.components.progress import render_progress

st.set_page_config(page_title="GEO POC", layout="wide")

init_session_state()
render_progress()

st.title("GEO / AI Visibility Proof of Concept")

st.markdown(
    """
Welcome to the GEO proof of concept.

Use the sidebar to move through the workflow:
1. Business Intake  
2. Prompt Targeting  
3. GEO Audit  
4. Content Optimiser  
5. Entities + Schema  
6. Summary  
"""
)
