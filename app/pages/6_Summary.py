import json
import streamlit as st
import app.bootstrap  # noqa: F401

from app.utils.session_state import init_session_state
from app.components.progress import render_progress
from core.report_builder import build_summary_markdown

st.set_page_config(page_title="Summary", layout="wide")
init_session_state()
render_progress()

st.title("6. Summary / Export")

required = [
    st.session_state.prompt_map,
    st.session_state.audit_result,
    st.session_state.entity_output,
    st.session_state.schema_output,
]

if not all(required):
    st.warning("Please complete the earlier stages first.")
    st.stop()

if st.button("Generate summary report"):
    st.session_state.summary_markdown = build_summary_markdown(
        st.session_state.intake,
        st.session_state.prompt_map,
        st.session_state.audit_result,
        st.session_state.entity_output,
        st.session_state.schema_output,
    )
    st.success("Summary report generated.")

if st.session_state.summary_markdown:
    st.markdown(st.session_state.summary_markdown)

    st.download_button(
        label="Download summary as .md",
        data=st.session_state.summary_markdown,
        file_name="geo_summary_report.md",
        mime="text/markdown",
    )

    st.download_button(
        label="Download schema as .json",
        data=json.dumps(st.session_state.schema_output["dict"], indent=2),
        file_name="schema.json",
        mime="application/json",
    )
