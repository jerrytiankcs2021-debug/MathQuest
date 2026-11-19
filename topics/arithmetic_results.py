import pandas as pd
import streamlit as st


def render_results(go_home, play_again):
    st.subheader("Congratulations!")

    score = st.session_state.correct_count
    total = st.session_state.total_questions
    percentage = round(score / total * 100)

    elapsed_time = (
        st.session_state.end_time
        - st.session_state.start_time
    )

    st.success(
        f"You got {score} out of {total} questions correct!"
    )

    st.write(f"Final score: {percentage}%")

    minutes = int(elapsed_time // 60)
    seconds = elapsed_time % 60

    st.write(
        f"Time taken: {minutes} min {seconds:.1f} sec"
    )

    st.subheader("Quiz Summary")

    df = pd.DataFrame(st.session_state.list_results)

    df = df.rename(columns={
        "question": "Question",
        "user_answer": "Your Answer",
        "correct_answer": "Correct Answer"
    })

    df.insert(
        0,
        "No.",
        range(1, len(df) + 1)
    )

    df["Result"] = df["is_correct"].map({
        True: "✅ Correct",
        False: "❌ Incorrect"
    })

    df = df[
        [
            "No.",
            "Question",
            "Correct Answer",
            "Your Answer",
            "Result"
        ]
    ]

    render_summary(df)

    if percentage >= 80:
        st.success("Great job!")

    elif percentage >= 60:
        st.warning("Good try! Keep practicing!")

    elif percentage == 0:
        st.error("Are we serious?")

    else:
        st.error("What happened? You can do better!")

    col1, col2 = st.columns(2)

    with col1:
        st.button("Play Again", on_click=play_again)

    with col2:
        st.button("Main Menu", on_click=go_home)


def render_summary(df):
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder
    except ModuleNotFoundError as exc:
        if exc.name != "st_aggrid":
            raise
        st.dataframe(df, hide_index=True, width="stretch")
        return

    gb = GridOptionsBuilder.from_dataframe(df)

    gb.configure_default_column(
        cellStyle={"textAlign": "center"},
        headerClass="center-header",
        sortable=True,
        filter=True,
        resizable=True
    )

    grid_options = gb.build()

    table_height = min(45 + len(df) * 36, 620)

    AgGrid(
        df,
        gridOptions=grid_options,
        height=table_height,
        columns_auto_size_mode="FIT_ALL_COLUMNS_TO_VIEW",
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
