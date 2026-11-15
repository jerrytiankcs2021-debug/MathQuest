import pandas as pd 
import streamlit as st
from main import generate_numbers, calculate_answer, check_answer
import time
from st_aggrid import AgGrid, GridOptionsBuilder



st.set_page_config(page_title="MathQuest", layout="wide")

# Initialize quiz memory
if "list_results" not in st.session_state:
    st.session_state.list_results = []

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "quiz_finished" not in st.session_state:
    st.session_state.quiz_finished = False

if "question_number" not in st.session_state:
    st.session_state.question_number = 1

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 5

if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "answer_input" not in st.session_state:
    st.session_state.answer_input = ""

if "feedback" not in st.session_state:
    st.session_state.feedback = ""


# Generate a new math question
def new_question():
    num_1, num_2 = generate_numbers(
        st.session_state.difficulty_code
    )

    if st.session_state.operation_code == "/":
        num_1 = num_1 * num_2
    
    st.session_state.num_1 = num_1
    st.session_state.num_2 = num_2


    st.session_state.correct_answer = calculate_answer(
        num_1,
        num_2,
        st.session_state.operation_code
    )

    st.session_state.answered = False
    st.session_state.feedback = ""


def clear_answer():
    st.session_state.answer_input = ""

# Process an answer and clear the input
def submit_answer():
    user_answer = st.session_state.answer_input.strip()

    if st.session_state.answered:
        return

    try:
        answer = int(user_answer)
    except ValueError:
        st.session_state.feedback = "Please enter a valid integer."
        return

    st.session_state.answered = True
    st.session_state.list_results.append({
        "question": f"{st.session_state.num_1} "
                    f"{st.session_state.operation_code} "
                    f"{st.session_state.num_2} =",
                    
        "user_answer": answer,
        "correct_answer": st.session_state.correct_answer
        })

    if check_answer(answer, st.session_state.correct_answer):
        st.session_state.correct_count += 1
        st.session_state.feedback = "Correct!"
    else:
        st.session_state.feedback = (
            f"Incorrect! The correct answer is "
            f"{st.session_state.correct_answer}."
        )


# Welcome message
st.title("MathQuest")
st.write("Welcome to MathQuest! Made by MiMi.")


# Quiz settings
col1, col2 = st.columns(2, gap="large")

with col1:
    operation = st.radio(
        "Choose an operation:",
        ["Addition", "Subtraction", "Multiplication", "Division"],
        disabled=st.session_state.quiz_started
    )

with col2:
    difficulty = st.radio(
        "Choose a difficulty level:",
        ["Easy", "Medium"],
        disabled=st.session_state.quiz_started
    )

num_questions = st.number_input(
    "How many questions?",
    min_value=1,
    value=5,
    step=1,
    format="%d",
    disabled=st.session_state.quiz_started
)


# Start a new quiz
if st.button(
    "Start Quiz",
    disabled=st.session_state.quiz_started
):
    st.session_state.list_results = []
    st.session_state.quiz_started = True
    st.session_state.quiz_finished = False
    st.session_state.question_number = 1
    st.session_state.total_questions = int(num_questions)
    st.session_state.correct_count = 0
    st.session_state.start_time = time.time()

    if operation == "Addition":
        st.session_state.operation_code = "+"
    elif operation == "Subtraction":
        st.session_state.operation_code = "-"
    elif operation == "Multiplication":
        st.session_state.operation_code = "x"
    else:
        st.session_state.operation_code = "/"

    if difficulty == "Easy":
        st.session_state.difficulty_code = "1"
    else:
        st.session_state.difficulty_code = "2"

    new_question()
    st.rerun()


# Display the current question
if st.session_state.quiz_started:

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
        f"What is {st.session_state.num_1} "
        f"{st.session_state.operation_code} "
        f"{st.session_state.num_2} = ?"
    )

    # Enter submits the form
    with st.form("answer_form", clear_on_submit=False):
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

    # Clear the answer box before creating the widget
    if st.session_state.get("clear_input_next", False):
        st.session_state.clear_input_next = False 
    
    # Display feedback
    if st.session_state.feedback:
        if st.session_state.feedback == "Correct!":
            st.success(st.session_state.feedback)
        elif st.session_state.answered:
            st.error(st.session_state.feedback)
        else:
            st.warning(st.session_state.feedback)

    # Move to the next question or finish
    if st.button(
        "Next Question"
        if st.session_state.question_number < st.session_state.total_questions
        else "Finish Quiz",
        disabled=not st.session_state.answered,
        on_click=clear_answer
    ): 

        if (
            st.session_state.question_number
            < st.session_state.total_questions
        ):
            st.session_state.question_number += 1
            st.session_state.clear_input_next = True
            new_question()
        else:
            st.session_state.quiz_started = False
            st.session_state.quiz_finished = True
            st.session_state.end_time = time.time()

        st.rerun()


# Final results screen
if st.session_state.quiz_finished:

    st.subheader("Congratulations!")

    score = st.session_state.correct_count
    total = st.session_state.total_questions
    percentage = round(score / total * 100)

    elapsed_time = (
        st.session_state.end_time
        - st.session_state.start_time
    )

    st.success(
        f"You got {score} out of {total} "
        f"questions correct!"
    )

    st.write(f"Final score: {percentage}%")

    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    st.subheader("Quiz Summary")
    
    # Create the DataFrame
    df = pd.DataFrame(st.session_state.list_results)

    # Rename columns
    df = df.rename(columns={
        "question": "Question",
        "user_answer": "Your Answer",
        "correct_answer": "Correct Answer"
    })

    # Add question numbers
    df.insert(0, "No.", range(1, len(df) + 1))

    # Add correct/incorrect result
    df["Result"] = df.apply(
        lambda row: "✅ Correct"
        if row["Your Answer"] == row["Correct Answer"]
        else "❌ Incorrect",
        axis=1
    )

    # Arrange columns
    df = df[["No.", "Question", "Correct Answer", "Your Answer", "Result"]]

    gb = GridOptionsBuilder.from_dataframe(df)

    
    gb.configure_default_column(
        cellStyle={"textAlign": "center"},
        headerClass="center-header",
        sortable=True,
        filter=True,
        resizable=True
    )

    grid_options = gb.build()

    table_height = 45 + len(df) * 36

    AgGrid(
        df,
        gridOptions=grid_options,
        height=table_height,
        fit_columns_on_grid_load=True,
        custom_css={
            ".ag-header-cell-label": {
                "justify-content": "center !important",
                "width": "100%"
            },
            ".ag-header-cell-text": {
                "text-align": "center !important",
                "width": "100%"
            }
        }
    )

    if percentage >= 80:
        st.success("Great job!")
    elif percentage >= 60:
        st.warning("Good try! Keep practicing!")
    elif percentage == 0:
            st.error("Are we serious?") 
    else:
        st.error("What happened? You can do better!")
    

    st.write(f"Time taken: {minutes} min {seconds:.1f} sec")

    if st.button("Play Again"):
        st.session_state.quiz_finished = False
        st.session_state.question_number = 1
        st.session_state.correct_count = 0
        st.session_state.answered = False
        st.session_state.feedback = ""
        st.rerun()
