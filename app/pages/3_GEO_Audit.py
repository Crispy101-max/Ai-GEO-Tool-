import streamlit as st
import app.bootstrap  # noqa: F401

from app.utils.session_state import init_session_state
from app.components.progress import render_progress
from core.audit_engine import run_geo_audit

st.set_page_config(page_title="GEO Audit", layout="wide")
init_session_state()
render_progress()

st.title("3. GEO Audit")

if not st.session_state.prompt_map:
    st.warning("Please generate the prompt map first.")
    st.stop()

url = st.text_input("URL to audit", value=st.session_state.intake.get("website_url", ""))

if st.button("Run audit"):
    if not url:
        st.error("Please enter a URL.")
    else:
        st.session_state.audit_result = run_geo_audit(url, st.session_state.prompt_map)

audit_result = st.session_state.audit_result

if audit_result:
    if not audit_result.get("ok", False):
        st.error(audit_result.get("error", "Audit failed."))
        st.stop()

    score = audit_result.get("overall_score", 0)
    st.metric("Overall GEO score", score)

    st.subheader("Top issues")
    for issue in audit_result.get("top_issues", []):
        st.markdown(f"- {issue}")

    st.subheader("Section diagnostics")
    for i, section in enumerate(audit_result.get("sections", []), start=1):
        with st.expander(f"{i}. {section['title']} — score {section['score']}"):
            st.markdown("**Supported prompts**")
            if section["supported_prompts"]:
                for prompt in section["supported_prompts"]:
                    st.markdown(f"- {prompt}")
            else:
                st.markdown("_No clear supported prompts found._")

            st.markdown("**Issues**")
            for issue in section["issues"]:
                st.markdown(f"- {issue}")

            st.markdown("**Current content**")
            st.write(section["content"])
else:
    st.info("Run the audit to analyse the page.")
