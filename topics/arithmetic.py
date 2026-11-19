import math
import time

import streamlit as st
import streamlit.components.v1 as components

from core.calculations import calculate_answer, check_answer
from main import generate_numbers
from topics.arithmetic_results import render_results


def show_choices():
    st.session_state.page = "choices"


def show_settings(number_type=None):
    if number_type is not None:
        st.session_state.number_type = number_type
    st.session_state.page = "settings"


def clear_answer():
    st.session_state.answer_input = ""


def new_question():
    num_1, num_2 = generate_numbers(
        st.session_state.difficulty_code,
        st.session_state.number_type
    )

    if st.session_state.operation_code == "/":
        num_1 = round(num_1 * num_2, 2)

    st.session_state.num_1 = num_1
    st.session_state.num_2 = num_2

    st.session_state.correct_answer = calculate_answer(
        num_1,
        num_2,
        st.session_state.operation_code
    )

    st.session_state.answered = False
    st.session_state.feedback = ""


def submit_answer():
    if st.session_state.answered:
        return

    user_answer = st.session_state.answer_input.strip()

    try:
        answer = float(user_answer)

        if not math.isfinite(answer):
            raise ValueError

    except ValueError:
        st.session_state.feedback = (
            "Please enter a valid number."
        )
        return

    correct_answer = st.session_state.correct_answer
    is_correct = check_answer(answer, correct_answer)

    st.session_state.answered = True

    st.session_state.list_results.append({
        "question": (
            f"{st.session_state.num_1} "
            f"{st.session_state.operation_code} "
            f"{st.session_state.num_2} ="
        ),
        "user_answer": answer,
        "correct_answer": correct_answer,
        "is_correct": is_correct
    })

    if is_correct:
        st.session_state.correct_count += 1
        st.session_state.feedback = "Correct!"
    else:
        st.session_state.feedback = (
            f"Incorrect! The correct answer is "
            f"{correct_answer:.10g}."
        )


def next_question():
    clear_answer()

    if (
        st.session_state.question_number
        < st.session_state.total_questions
    ):
        st.session_state.question_number += 1
        new_question()

    else:
        st.session_state.end_time = time.time()
        st.session_state.page = "results"


def render_choices(go_home):
    st.button("Main Menu", on_click=go_home)
    st.header("Arithmetic")
    st.write("Which kind of numbers would you like to practice?")

    columns = st.columns(2)
    for column, number_type in zip(columns, ("Whole Numbers", "Decimals")):
        with column:
            st.button(
                number_type,
                on_click=show_settings,
                args=(number_type,),
                width="stretch",
            )


def render_settings():

    st.button("Back to Arithmetic", on_click=show_choices)

    st.subheader(
        f"{st.session_state.number_type} Quiz Settings"
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        operation = st.radio(
            "Choose an operation:",
            [
                "Addition",
                "Subtraction",
                "Multiplication",
                "Division"
            ]
        )

    with col2:
        difficulty = st.radio(
            "Choose a difficulty level:",
            ["Easy", "Medium"]
        )

    with st.form(
        "quiz_settings_form",
        enter_to_submit=True
    ):
        num_questions = st.text_input(
            "How many questions?",
            value="5",
            placeholder="Press Enter to Start Quiz"
        )

        start_quiz = st.form_submit_button(
            "Start Quiz"
        )

    if start_quiz:

        try:
            total = int(num_questions)

            if total < 1 or total > 100:
                raise ValueError

        except ValueError:
            st.error(
                "Please enter a whole number "
                "between 1 and 100."
            )
            st.stop()

        operations = {
            "Addition": "+",
            "Subtraction": "-",
            "Multiplication": "x",
            "Division": "/"
        }

        st.session_state.operation_code = operations[operation]

        st.session_state.difficulty_code = (
            "1" if difficulty == "Easy" else "2"
        )

        st.session_state.list_results = []
        st.session_state.question_number = 1
        st.session_state.total_questions = total
        st.session_state.correct_count = 0
        st.session_state.start_time = time.time()

        clear_answer()
        new_question()

        st.session_state.page = "quiz"
        st.rerun()


def focus_quiz_control():
    state = st.session_state
    selector = (
        ".st-key-quiz_continue button:not(:disabled)"
        if state.answered
        else ".st-key-quiz_answer input:not(:disabled)"
    )
    # Refresh the iframe for each question and when validation requests a retry.
    phase = "continue" if state.answered else "retry" if state.feedback else "answer"
    components.html(
        f"""
        <!-- Quiz {state.start_time}, question {state.question_number}, phase {phase} -->
        <script>
        const page = window.parent;
        const selector = "{selector}";
        const deadline = performance.now() + 2000;
        function focusControl(previousControl) {{
            const control = page.document.querySelector(selector);
            if (control && control.getClientRects().length) {{
                if (previousControl === control && page.document.activeElement === control) return;
                if (page.document.activeElement !== control) control.focus();
            }}
            if (performance.now() < deadline) {{
                page.requestAnimationFrame(() => focusControl(control));
            }}
        }}
        // Wait until the surrounding Streamlit widgets have been painted.
        page.requestAnimationFrame(() => page.requestAnimationFrame(() => focusControl(null)));
        </script>
        """,
        height=0,
        tab_index=-1,
    )


def render_quiz():
    st.subheader(
        f"{st.session_state.number_type} Quiz"
    )

    progress = (
        st.session_state.question_number - 1
        + int(st.session_state.answered)
    ) / st.session_state.total_questions

    st.progress(progress)

    st.write(
        f"Question {st.session_state.question_number} "
        f"of {st.session_state.total_questions}"
    )

    st.subheader(
        f"{st.session_state.num_1} "
        f"{st.session_state.operation_code} "
        f"{st.session_state.num_2} = ?"
    )

    # ENTER OR CLICK TO SUBMIT
    with st.container(key="quiz_answer"), st.form(
        "answer_form",
        enter_to_submit=True
    ):

        st.text_input(
            "Your answer:",
            placeholder="Enter your answer here",
            key="answer_input",
            disabled=st.session_state.answered
        )

        st.form_submit_button(
            "Submit Answer",
            on_click=submit_answer,
            disabled=st.session_state.answered
        )

    # FEEDBACK
    if st.session_state.feedback:

        if st.session_state.feedback == "Correct!":
            st.success(st.session_state.feedback)

        elif st.session_state.answered:
            st.error(st.session_state.feedback)

        else:
            st.warning(st.session_state.feedback)

    # NEXT QUESTION / FINISH
    if st.session_state.answered:
        with st.container(key="quiz_continue"):
            st.button(
                "Next Question"
                if st.session_state.question_number < st.session_state.total_questions
                else "Finish Quiz",
                on_click=next_question,
            )

    focus_quiz_control()


def render(go_home):
    page = st.session_state.get("page", "choices")
    st.title("MathQuest", anchor=False)
    if page == "choices":
        render_choices(go_home)
    elif page == "settings":
        render_settings()
    elif page == "quiz":
        render_quiz()
    elif page == "results":
        render_results(go_home, show_settings)
