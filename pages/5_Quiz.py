from utils.ai_engine import ask_ai
import streamlit as st

st.set_page_config(
    page_title="Quiz Generator",
    page_icon="❓",
    layout="wide"
)

st.title("❓ AI Quiz Generator")

st.write("Generate AI-based MCQs from your study material.")

st.divider()

content = st.text_area(
    "📚 Enter Topic or Notes",
    height=250,
    placeholder="Example: Explain Neural Networks..."
)

difficulty = st.selectbox(
    "🎯 Select Difficulty",
    ["Easy", "Medium", "Hard"]
)

number = st.slider(
    "Number of Questions",
    1,
    10,
    5
)

if st.button("🚀 Generate Quiz"):

    if content:

        with st.spinner("🤖 Creating Quiz..."):

            prompt = f"""
You are an expert teacher.

Create exactly {number} {difficulty} level MCQs from the following notes.

Rules:
- Every question must have 4 options (A, B, C, D).
- Only one correct answer.
- Questions must be based only on the notes.
- Do not repeat questions.
- Return only the quiz.

Notes:
{content}
"""

            quiz = ask_ai(prompt)

            st.success("✅ Quiz Generated Successfully!")

            st.markdown(quiz)

    else:
        st.warning("⚠ Please enter notes/topic first.")

st.divider()

st.info("""
🚀 Features:
- AI MCQ Generation
- Automatic Answers
- Difficulty Selection
- Groq AI Powered
""")