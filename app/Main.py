import streamlit as st
import app.bootstrap  # noqa: F401

from app.utils.session_state import init_session_state
from app.components.progress import render_progress

st.set_page_config(page_title="GEO POC", layout="wide")

init_session_state()
render_progress()

st.title("GEO / AI Visibility Proof of Concept")
st.markdown(
    """
Welcome to the MVP workflow.

Use the left-hand page navigation to move through the stages:

1. Business Intake  
2. Prompt Targeting  
3. GEO Audit  
4. Content Optimiser  
5. Entities + Schema  
6. Summary  
"""
)

with st.expander("Current session data"):
    st.json({
        "intake": st.session_state.intake,
        "has_prompt_map": st.session_state.prompt_map is not None,
        "has_audit_result": st.session_state.audit_result is not None,
        "has_optimised_output": st.session_state.optimised_output is not None,
        "has_entity_output": st.session_state.entity_output is not None,
        "has_schema_output": st.session_state.schema_output is not None,
    })


