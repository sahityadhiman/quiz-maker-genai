import os

import streamlit as st
from google import genai


st.set_page_config(page_title="AI quiz maker", page_icon="📝")
st.title("📝 AI quiz maker")
st.caption("Turn a topic or your study notes into a multiple-choice quiz.")

api_key = os.getenv("GEMINI_API_KEY", "").strip()
model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")fallback_model = os.getenv("GEMINI_FALLBACK_MODEL", "gemini-3.5-flash-lite")


def generate_with_fallback(client, prompt):
    models = list(dict.fromkeys([model, fallback_model]))
    for index, candidate in enumerate(models):
        try:
            return client.models.generate_content(model=candidate, contents=prompt)
        except Exception as exc:
            error = str(exc).upper()
            transient_overload = any(code in error for code in ("429", "500", "502", "503", "504", "UNAVAILABLE", "RESOURCE_EXHAUSTED"))
            if not transient_overload or index == len(models) - 1:
                raise
            st.info(f"{candidate} is temporarily unavailable. Trying {models[index + 1]}…")


def generation_error(exc):
    error = str(exc).upper()
    if "503" in error or "UNAVAILABLE" in error or "500" in error or "502" in error or "504" in error:
        return "Gemini is temporarily busy on the available models. Please wait a moment and try again."
    if "429" in error or "RESOURCE_EXHAUSTED" in error:
        return "The Gemini request limit has been reached. Please try again later."
    return str(exc)

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
        st.error("Gemini is not configured for this app. Please contact the app owner.")
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
                response = generate_with_fallback(client, prompt)
            st.session_state.quiz = (response.text or "The model returned an empty response.").strip()
        except Exception as exc:
            st.error(f"Could not generate the quiz: {generation_error(exc)}")

if st.session_state.get("quiz"):
    st.subheader("Your quiz")
    st.markdown(st.session_state.quiz)
    st.download_button(
        "Download quiz as Markdown",
        data=st.session_state.quiz,
        file_name="study_quiz.md",
        mime="text/markdown",
    )
