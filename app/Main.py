import streamlit as st

from app.utils.session_state import init_session_state

st.set_page_config(page_title="GEO POC", layout="wide")

init_session_state()

st.title("GEO POC")
st.write("Use the sidebar to navigate through the workflow.")

st.markdown(
    """
    ### Workflow
    1. Business Intake
    2. Prompt Targeting
    3. GEO Audit
    4. Content Optimiser
    5. Entities Schema
    6. Summary
    """
)
