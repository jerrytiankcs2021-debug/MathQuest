# MathQuest

MathQuest is a Streamlit practice site for Whole Numbers and Decimals. Choose Arithmetic, pick a number type, and set the operation, difficulty, and number of questions. Geometry, Algebra, and SSAT Practice are marked Coming Soon.

## Run locally

Open Terminal in this project folder. Use Python 3.12 so your local setup matches the deployment settings below.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open [MathQuest locally](http://localhost:8501). To stop the server, press Ctrl+C in Terminal.

## Deploy on Streamlit Community Cloud

1. Commit and push this folder's contents to a GitHub repository you administer. Keep `app.py`, `requirements.txt`, and `style.css` at the repository root. Include `main.py`, `home.py`, `core/`, `topics/`, and the hidden `.streamlit/` directory. Use a public repository if you want the source and app to be public.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/) and connect GitHub. Choose **Create app**, then **Yup, I have an app**.
3. Choose your repository and branch, usually `main`, and enter `app.py` in **Main file path**.
4. In **Advanced settings**, select Python **3.12**. Leave the secrets field empty. Save the settings and select **Deploy**.
5. Open the assigned `streamlit.app` address and finish a short quiz in each number type to check that the results table loads.

See the [Community Cloud deployment guide](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy).

## Add a topic

Put the topic's interface in its own module in `topics/`, with a `render(go_home)` function. Register that function on the matching entry in `home.py` to replace its Coming Soon label with a working button. The `go_home` callback returns the learner to the homepage.

- `app.py` loads the styles and routes to the selected topic.
- `topics/arithmetic.py` handles quiz settings, questions, feedback, and progress.
- `topics/arithmetic_results.py` presents the score, time, and answer-by-answer summary.
- `main.py` dispatches number generation to `topics/whole_numbers.py` or `topics/decimals.py`. Both use the shared math functions in `core/calculations.py` through the quiz.

Results are kept in the current browser session. Use **Play Again** to set up a new quiz in the same number type.
