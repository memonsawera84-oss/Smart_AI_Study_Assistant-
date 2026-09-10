import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.ai_engine import ask_ai

# Import RAG Engine
from rag.rag_engine import RAGEngine

# ==========================================
# Page Configuration
# ==========================================
st.set_page_config(
    page_title="Smart PDF Assistant",
    page_icon="📄",
    layout="wide"
)

# ==========================================
# Custom CSS
# ==========================================
st.markdown("""
<style>

.main{
    padding-top:20px;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-size:16px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# Title
# ==========================================
st.title("📄 Smart AI PDF Assistant")

st.markdown("""
Upload your study material and chat with your PDF using Artificial Intelligence.
""")

st.divider()

# ==========================================
# Upload PDF
# ==========================================
uploaded_file = st.file_uploader(
    "📂 Upload PDF",
    type=["pdf"]
)

# ==========================================
# If PDF Uploaded
# ==========================================
if uploaded_file:

    # Extract text
    text = extract_text_from_pdf(uploaded_file)

    if not text.strip():
        st.error("❌ No text found in PDF.")
        st.stop()

    st.success("✅ PDF Uploaded Successfully")
    st.write("📄 File Name:", uploaded_file.name)
    st.write("📦 File Size:", round(uploaded_file.size / 1024, 2), "KB")

    # ==========================================
    # Build RAG Database
    # ==========================================

    rag = RAGEngine()

    with st.spinner("🔄 Preparing AI Knowledge Base..."):

        total_chunks = rag.build_database(text)
    st.success(f"✅ RAG Database Created ({total_chunks} chunks)")
    st.success(f"✅ Knowledge Base Ready ({total_chunks} Chunks)")

    # ==========================================
    # Create Tabs
    # ==========================================

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📖 Document",
            "📝 Summary",
            "❓ Quiz",
            "💬 PDF Chat"
        ]
    )

    # ==========================================
    # TAB 1
    # ==========================================

    with tab1:

        st.subheader("📄 PDF Content")

        st.text_area(
            "Extracted Text",
            text,
            height=450
        )

    # ==========================================
    # TAB 2
    # ==========================================

    with tab2:

      st.subheader("📝 AI Summary")

    if st.button("Generate Summary"):

        with st.spinner("Generating Summary..."):

            prompt = f"""
Summarize the following PDF in simple student-friendly language.

{text}
"""
        with st.spinner("📝 Generating Summary..."):
            summary = ask_ai(prompt)

        st.success("Summary Generated Successfully")

        st.write(summary)

        st.download_button(
            "📥 Download Summary",
            data=summary,
            file_name="summary.txt",
            mime="text/plain"
        )
        # ==========================================
    # TAB 3 - AI QUIZ
    # ==========================================

    with tab3:

        st.subheader("❓ AI Quiz Generator")

        if st.button("Generate Quiz"):

            with st.spinner("Generating Quiz..."):

                prompt = f"""
Generate 10 Multiple Choice Questions from the given context.

Each question must include:

Question:
A.
B.
C.
D.

Correct Answer:
Explanation:

Context:

{text}
"""
            with st.spinner("❓ Generating Quiz..."):
                quiz = ask_ai(prompt)

            st.success("Quiz Generated Successfully")

            st.write(quiz)
            st.download_button(
                "📥 Download Quiz",
                data=quiz,
                file_name="quiz.txt",
                mime="text/plain"
            )
    # ==========================================
    # TAB 4 - RAG PDF CHAT
    # ==========================================

    with tab4:

        st.subheader("💬 Chat with your PDF (RAG)")

        question = st.text_input(
            "Ask anything from this PDF",
            placeholder="Example: What is Machine Learning?"
        )

        if st.button("🚀 Ask AI"):

            if question.strip():

                with st.spinner("Searching relevant information..."):

                    # --------------------------------------
                    # Find Relevant Chunks
                    # --------------------------------------

                    chunks = rag.search(question)

                    # Convert list into one string
                    context = "\n\n".join(chunks)

                    # --------------------------------------
                    # Final Prompt
                    # --------------------------------------

                    prompt = f"""
You are a Smart AI Study Assistant.

Answer ONLY from the context below.

If the answer is not available in the context, say:

"I could not find this information in the uploaded PDF."

Context:

{context}

Question:

{question}
"""
                with st.spinner("🤖 Finding Answer..."):
                    answer = ask_ai(prompt)

                st.success("✅ Answer Generated")

                st.write(answer)

                # --------------------------------------
                # Show Retrieved Chunks
                # --------------------------------------

                with st.expander("📚 View Retrieved PDF Chunks"):

                    for i, chunk in enumerate(chunks, start=1):

                        st.markdown(f"### Chunk {i}")

                        st.write(chunk)

            else:

                st.warning("Please enter a question.")        