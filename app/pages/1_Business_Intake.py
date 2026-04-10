import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "app" / "components"))
sys.path.insert(0, str(_ROOT / "app" / "utils"))

import streamlit as st
from session_state import init_session_state
from progress import render_progress

st.title("1. Business Intake")

with st.form("business_intake_form"):
    website_url = st.text_input("Website URL", st.session_state.intake.get("website_url", ""))
    business_name = st.text_input("Business name", st.session_state.intake.get("business_name", ""))
    industry = st.text_input("Industry", st.session_state.intake.get("industry", ""))
    niche = st.text_input("Niche", st.session_state.intake.get("niche", ""))
    target_audience = st.text_area("Target audience", st.session_state.intake.get("target_audience", ""))
    products_services = st.text_area("Products / services", st.session_state.intake.get("products_services", ""))
    differentiators = st.text_area("Differentiators", st.session_state.intake.get("differentiators", ""))
    recommendation_goals = st.text_area(
        "What the client wants to be recommended for",
        st.session_state.intake.get("recommendation_goals", "")
    )
    external_ai_visibility_data = st.text_area(
        "External AI visibility data (optional)",
        st.session_state.intake.get("external_ai_visibility_data", "")
    )

    submitted = st.form_submit_button("Save intake")

if submitted:
    st.session_state.intake = {
        "website_url": website_url,
        "business_name": business_name,
        "industry": industry,
        "niche": niche,
        "target_audience": target_audience,
        "products_services": products_services,
        "differentiators": differentiators,
        "recommendation_goals": recommendation_goals,
        "external_ai_visibility_data": external_ai_visibility_data,
    }
    st.success("Business intake saved.")

st.subheader("Current intake")
st.json(st.session_state.intake)
