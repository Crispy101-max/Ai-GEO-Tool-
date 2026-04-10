import streamlit as st


def init_session_state():
    defaults = {
        "intake": {},
        "prompt_targeting": {},
        "geo_audit": {},
        "content_optimiser": {},
        "entities_schema": {},
        "summary": {},
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
