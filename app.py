from pathlib import Path

import streamlit as st

from home import TOPICS, render_home


def go_home():
    st.session_state.topic = None
    st.session_state.page = "choices"


st.set_page_config(page_title="MathQuest", page_icon="🧮", layout="wide")
st.html(Path(__file__).with_name("style.css"))

topic = TOPICS.get(st.session_state.get("topic"))
if topic and topic.render:
    topic.render(go_home)
else:
    render_home()
