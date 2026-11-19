from dataclasses import dataclass
from typing import Callable, Optional

import streamlit as st

from topics import arithmetic


@dataclass(frozen=True)
class Topic:
    title: str
    description: str
    icon: str
    render: Optional[Callable[[Callable[[], None]], None]] = None


TOPICS = {
    "arithmetic": Topic(
        "Arithmetic", "Whole numbers and decimals", "calculate", arithmetic.render
    ),
    "geometry": Topic(
        "Geometry", "Triangles, area, Pythagorean theorem", "category"
    ),
    "algebra": Topic("Algebra", "Equations, exponents, square roots", "functions"),
    "ssat": Topic("SSAT Practice", "Middle and Upper Level", "school"),
}


def open_topic(topic_id):
    st.session_state.topic = topic_id
    st.session_state.page = "choices"


def render_home():
    with st.container(key="home", border=True):
        st.title("MathQuest", anchor=False)
        st.caption("Practice • Learn • Improve")
        with st.container(key="prompt"):
            st.header("What would you like to practice today?", anchor=False)
            st.write("Choose a topic, set your difficulty, and begin your quest.")

        topic_items = list(TOPICS.items())
        for start in range(0, len(topic_items), 2):
            row = topic_items[start:start + 2]
            for column, (topic_id, topic) in zip(st.columns(2), row):
                with column, st.container(key=f"card_{topic_id}", border=True):
                    st.markdown(f":material/{topic.icon}:")
                    st.subheader(topic.title, anchor=False)
                    st.write(topic.description)
                    if topic.render:
                        st.button(
                            f"Start {topic.title}",
                            type="primary",
                            on_click=open_topic,
                            args=(topic_id,),
                        )
                    else:
                        st.caption("Coming Soon")

        st.caption("Daily practice • Scores • Review mistakes")
