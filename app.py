import os

import streamlit as st
from google import genai


st.set_page_config(page_title="AI quiz maker", page_icon="📝")
st.title("📝 AI quiz maker")
st.caption("Turn a topic or your study notes into a multiple-choice quiz.")

server_api_key = os.getenv("GEMINI_API_KEY", "")
user_api_key = st.sidebar.text_input(
    "Gemini API key",
    value="",
    type="password",
    help="Enter your own key if the app owner has not configured one. It is not saved to the project files.",
)
api_key = user_api_key or server_api_key
if server_api_key:
    st.sidebar.caption("A server-managed key is configured. Requests share its quota.")
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
st.sidebar.caption(f"Model: {model}")

with st.form("quiz_form"):
    source = st.text_area(
        "Topic or study material",
        height=220,
        placeholder="Example: Photosynthesis — light reactions, chlorophyll, ATP, and the Calvin cycle…",
    )
    col1, col2 = st.columns(2)
    with col1:
        question_count = st.slider("Number of questions", min_value=3, max_value=10, value=5)
    with col2:
        difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
    submitted = st.form_submit_button("Generate quiz", type="primary")

if submitted:
    st.session_state.pop("quiz", None)
    if not source.strip():
        st.warning("Add a topic or study material first.")
    elif not api_key:
        st.error("Enter a Gemini API key in the sidebar first.")
    else:
        prompt = f"""Create a {difficulty.lower()}-level multiple-choice quiz with exactly {question_count} questions based on the input below. The input may be detailed study material or just a topic. If it is detailed material, base the questions only on that material. If it is only a topic or short phrase, use reliable standard knowledge about that topic. Avoid disputed claims.

For each question, provide four options labeled A–D. After all questions, include an answer key with the correct letter and a one-sentence explanation for each answer. Make the questions clear and avoid duplicates. Format the result in readable Markdown.

<topic_or_source_material>
{source}
</topic_or_source_material>
"""
        try:
            with st.spinner("Creating your quiz…"):
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(model=model, contents=prompt)
            st.session_state.quiz = (response.text or "The model returned an empty response.").strip()
        except Exception as exc:
            st.error(f"Could not generate the quiz: {exc}")

if st.session_state.get("quiz"):
    st.subheader("Your quiz")
    st.markdown(st.session_state.quiz)
    st.download_button(
        "Download quiz as Markdown",
        data=st.session_state.quiz,
        file_name="study_quiz.md",
        mime="text/markdown",
    )
