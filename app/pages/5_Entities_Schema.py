import streamlit as st
import app.bootstrap  # noqa: F401

from utils.session_state import init_session_state
from app.components.progress import render_progress
from core.entity_extractor import extract_entities
from core.schema_generator import generate_schema

st.set_page_config(page_title="Entities + Schema", layout="wide")
init_session_state()
render_progress()

st.title("5. Entities + Schema")

if not st.session_state.optimised_output:
    st.warning("Please generate the optimised content first.")
    st.stop()

col1, col2 = st.columns(2)

with col1:
    if st.button("Extract entities"):
        st.session_state.entity_output = extract_entities(
            st.session_state.intake,
            st.session_state.prompt_map,
            st.session_state.audit_result,
        )
        st.success("Entity extraction complete.")

with col2:
    if st.button("Generate schema"):
        st.session_state.schema_output = generate_schema(
            st.session_state.intake,
            st.session_state.prompt_map,
            st.session_state.optimised_output,
        )
        st.success("Schema generated.")

if st.session_state.entity_output:
    st.subheader("Entity output")
    st.json(st.session_state.entity_output)

if st.session_state.schema_output:
    st.subheader("JSON-LD schema")
    st.code(st.session_state.schema_output["json"], language="json")
