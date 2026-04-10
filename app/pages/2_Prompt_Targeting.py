import streamlit as st
import app.bootstrap  # noqa: F401

from utils.session_state import init_session_state
from app.components.progress import render_progress
from core.prompt_generator import generate_prompt_map

st.set_page_config(page_title="Prompt Targeting", layout="wide")
init_session_state()
render_progress()

st.title("2. Prompt Targeting")

if not st.session_state.intake.get("business_name") and not st.session_state.intake.get("website_url"):
    st.warning("Please complete Business Intake first.")
    st.stop()

if st.button("Generate prompt map"):
    st.session_state.prompt_map = generate_prompt_map(st.session_state.intake)
    st.success("Prompt map generated.")

prompt_map = st.session_state.prompt_map

if prompt_map:
    st.subheader("Generated prompts")

    for key, values in prompt_map.items():
        st.markdown(f"### {key.replace('_', ' ').title()}")
        edited = st.text_area(
            key,
            value="\n".join(values),
            height=180,
            key=f"edit_{key}",
            label_visibility="collapsed"
        )
        prompt_map[key] = [line.strip() for line in edited.split("\n") if line.strip()]

    st.session_state.prompt_map = prompt_map
    st.success("Prompt map is editable and saved in session state.")
else:
    st.info("Click 'Generate prompt map' to create your target prompts.")
