import streamlit as st


DEFAULTS = {
    "intake": {
        "website_url": "",
        "business_name": "",
        "industry": "",
        "niche": "",
        "target_audience": "",
        "products_services": "",
        "differentiators": "",
        "recommendation_goals": "",
        "external_ai_visibility_data": "",
    },
    "prompt_map": None,
    "audit_result": None,
    "optimised_output": None,
    "entity_output": None,
    "schema_output": None,
    "summary_markdown": None,
}


def init_session_state():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value
