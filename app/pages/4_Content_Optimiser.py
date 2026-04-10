import streamlit as st
import app.bootstrap  # noqa: F401

from utils.session_state import init_session_state
from app.components.progress import render_progress
from core.optimiser import optimise_content

st.set_page_config(page_title="Content Optimiser", layout="wide")
init_session_state()
render_progress()

st.title("4. Content Optimiser")

if not st.session_state.audit_result or not st.session_state.audit_result.get("ok", False):
    st.warning("Please run the GEO audit first.")
    st.stop()

if st.button("Generate optimised content"):
    st.session_state.optimised_output = optimise_content(
        st.session_state.audit_result,
        st.session_state.intake,
        st.session_state.prompt_map,
    )
    st.success("Optimised content generated.")

optimised_output = st.session_state.optimised_output

if optimised_output:
    st.metric("Original score", optimised_output.get("overall_score_before", 0))
    st.subheader("Before vs after")

    for section in optimised_output.get("sections", []):
        with st.expander(section["title"]):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Original")
                st.write(section["original"])

            with col2:
                st.markdown("### Rewritten")
                st.markdown(section["rewritten"])

            st.markdown("**Issues addressed**")
            for issue in section.get("issues", []):
                st.markdown(f"- {issue}")

            st.markdown("**Supported prompts**")
            for prompt in section.get("supported_prompts", []):
                st.markdown(f"- {prompt}")
else:
    st.info("Generate optimised content after the audit.")
