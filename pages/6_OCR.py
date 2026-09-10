import streamlit as st
from utils.ocr import extract_text_from_image
from utils.ai_engine import ask_ai

st.set_page_config(
    page_title="OCR Assistant",
    page_icon="🖼",
    layout="wide"
)

st.title("🖼 AI OCR Assistant")

uploaded_image = st.file_uploader(
    "Upload an Image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_image:

    st.image(uploaded_image, use_container_width=True)

    text = extract_text_from_image(uploaded_image)

    st.success("✅ Text Extracted Successfully")

    st.subheader("📄 Extracted Text")

    st.text_area(
        "OCR Output",
        text,
        height=250
    )

    col1, col2 = st.columns(2)

    # ================= Summary =================

    with col1:

        if st.button("📝 Generate Summary"):

            with st.spinner("Generating Summary..."):

                prompt = f"""
Summarize these notes in simple student-friendly language.

{text}
"""

                summary = ask_ai(prompt)

                st.subheader("📚 Summary")

                st.write(summary)

    # ================= Quiz =================

    with col2:

        if st.button("❓ Generate Quiz"):

            with st.spinner("Generating Quiz..."):

                prompt = f"""
Create 5 multiple-choice questions from these notes.

Rules:
- Four options (A, B, C, D)
- Mention the correct answer.
- Return only the quiz.

Notes:

{text}
"""

                quiz = ask_ai(prompt)

                st.subheader("📝 Quiz")

                st.markdown(quiz)