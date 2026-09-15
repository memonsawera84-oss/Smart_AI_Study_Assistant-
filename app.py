import streamlit as st
# ================= SIDEBAR ROBOT STYLE =================

st.markdown("""
<style>

/* Sidebar background */
section[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #031b4e 0%,
        #062d6f 50%,
        #031536 100%
    );
}

/* Robot image */
section[data-testid="stSidebar"] img {
    width: 150px !important;
    height: 150px !important;
    object-fit: contain;
    display: block;
    margin: 5px auto 10px auto;
    border-radius: 50%;
    filter: drop-shadow(0 0 8px #00e5ff)
            drop-shadow(0 0 18px #2979ff);
}

/* Sidebar title */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: white;
}

/* Sidebar text */
section[data-testid="stSidebar"] p {
    color: #d9e8ff;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Smart AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main hero box */
.hero {
    background: linear-gradient(135deg, #0d47a1, #1976d2, #42a5f5);
    padding: 40px;
    border-radius: 25px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(0, 80, 180, 0.20);
}

.hero h1 {
    color: white;
    font-size: 42px;
    margin-bottom: 10px;
}

.hero h3 {
    color: white;
    font-size: 23px;
    margin-bottom: 15px;
}

.hero p {
    color: white;
    font-size: 17px;
}

/* Feature boxes */
.feature-box {
    background: white;
    border: 1px solid #dce6f2;
    border-radius: 20px;
    padding: 24px;
    min-height: 185px;
    box-shadow: 0 5px 18px rgba(0, 0, 0, 0.06);
    margin-bottom: 20px;
}

.feature-box h3 {
    color: #123b70;
}

.feature-box p {
    color: #5f6f82;
    line-height: 1.5;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

# ================= SIDEBAR ROBOT =================

st.sidebar.image(
    "assets/robot.png"
)

st.sidebar.title("🎓 Smart AI")
st.sidebar.subheader("Study Assistant")
st.sidebar.caption("Learn • Practice • Grow")

st.sidebar.divider()

menu = st.sidebar.radio(
    "🧭 Navigation",
    [
        "🏠 Home",
        "🤖 AI Chat",
        "📄 PDF Assistant",
        "📝 Summarizer",
        "❓ Quiz Generator",
        "🔍 OCR",
        "🧠 Smart Study Planner",
        "📊 Progress Dashboard",
        "🎤 Advanced Voice Assistant",
        "🕘 History",
        "⚙️ Settings"
    ]
)


# =========================================================
# NAVIGATION
# =========================================================

if menu == "📄 PDF Assistant":
    st.switch_page("pages/3_PDF_Assistant.py")

elif menu == "🧠 Smart Study Planner":
    st.switch_page("pages/6_Smart_Study_Planner.py")

elif menu == "📊 Progress Dashboard":
    st.switch_page("pages/7_Progress_Dashboard.py")

elif menu == "🎤 Advanced Voice Assistant":
    st.switch_page("pages/9_Voice_Assistant.py")


# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    # -----------------------------------------------------
    # HERO BOX
    # -----------------------------------------------------

    # HERO BOX

    st.markdown("""
<div style="
padding:30px;
border-radius:20px;
background:linear-gradient(90deg,#4F46E5,#06B6D4);
color:white;
text-align:center;
box-shadow:0px 4px 15px rgba(0,0,0,0.2);
">
<h1>🎓 Smart AI Study Assistant</h1>
<h3>Your Personal AI Learning Companion</h3>
<p>Powered by Groq AI • RAG • EasyOCR • Streamlit</p>
</div>
""", unsafe_allow_html=True)

    # -----------------------------------------------------
    # LEARNING OVERVIEW
    # -----------------------------------------------------

    st.header("📊 Your Learning Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📄 PDFs Uploaded", "0")

    with col2:
        st.metric("📝 Summaries", "0")

    with col3:
        st.metric("❓ Quizzes", "0")

    with col4:
        st.metric("💬 AI Chats", "0")


    st.divider()


    # -----------------------------------------------------
    # FEATURES
    # -----------------------------------------------------

    st.header("🚀 AI Learning Features")

    st.write(
        "Everything you need to study smarter in one platform."
    )

    st.write("")


    # =====================================================
    # ROW 1
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown("## 📄 PDF Assistant")

            st.write(
                "Upload your PDF and get AI-powered "
                "explanations, summaries and answers."
            )


    with col2:

        with st.container(border=True):

            st.markdown("## 📝 Smart Summarizer")

            st.write(
                "Turn long study material into short "
                "and easy-to-understand summaries."
            )


    with col3:

        with st.container(border=True):

            st.markdown("## ❓ Quiz Generator")

            st.write(
                "Generate AI-powered MCQs and practice "
                "questions from your study material."
            )


    # =====================================================
    # ROW 2
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        with st.container(border=True):

            st.markdown("## 🤖 AI Chat")

            st.write(
                "Ask questions and receive intelligent "
                "student-friendly answers."
            )


    with col2:

        with st.container(border=True):

            st.markdown("## 🔍 OCR Reader")

            st.write(
                "Extract text from handwritten and "
                "printed study notes."
            )


    with col3:

        with st.container(border=True):

            st.markdown("## 🎤 Voice Assistant")

            st.write(
                "Advanced voice-based learning support "
                "for future enhancement."
            )


    # =====================================================
    # ROW 3
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown("## 🧠 Smart Study Planner")

            st.write(
                "Create personalized study plans according "
                "to your exam schedule."
            )


    with col2:

        with st.container(border=True):

            st.markdown("## 📊 Progress Dashboard")

            st.write(
                "Track topics, quiz performance, study "
                "progress and study time."
            )


    st.divider()


    # -----------------------------------------------------
    # ABOUT
    # -----------------------------------------------------

    st.header("📌 About Smart AI Study Assistant")

    with st.container(border=True):

        st.write(
            "Smart AI Study Assistant is a multimodal "
            "AI learning platform designed to help "
            "students learn faster, smarter and "
            "more effectively."
        )

        st.subheader("✨ Core Capabilities")

        col1, col2 = st.columns(2)

        with col1:
            st.write("✔ AI Chat")
            st.write("✔ PDF Analysis and RAG")
            st.write("✔ Smart Summarization")
            st.write("✔ Automatic Quiz Generation")

        with col2:
            st.write("✔ OCR for Study Notes")
            st.write("✔ Smart Study Planning")
            st.write("✔ Student Progress Dashboard")
            st.write("✔ Advanced Voice Assistant")


    st.divider()


    # -----------------------------------------------------
    # START LEARNING
    # -----------------------------------------------------

    st.header("🚀 Ready to Start Learning?")

    if st.button(
        "🚀 Start Learning",
        type="primary",
        use_container_width=True
    ):

        st.balloons()

        st.success(
            "🎉 Welcome to your AI learning journey!"
        )


    st.write("")

    st.caption(
        "© 2026 Smart AI Study Assistant | "
        "AI Powered Learning Platform"
    )


# =========================================================
# AI CHAT
# =========================================================

elif menu == "🤖 AI Chat":

    st.title("🤖 AI Chat")

    st.write(
        "Your AI learning assistant."
    )


# =========================================================
# SUMMARIZER
# =========================================================

elif menu == "📝 Summarizer":

    st.title("📝 Smart Summarizer")

    st.write(
        "Summarize your study material using AI."
    )


# =========================================================
# QUIZ
# =========================================================

elif menu == "❓ Quiz Generator":

    st.title("❓ Quiz Generator")

    st.write(
        "Generate practice questions from your study material."
    )


# =========================================================
# OCR
# =========================================================

elif menu == "🔍 OCR":

    st.title("🔍 OCR Reader")

    st.write(
        "Extract text from your study notes."
    )


# =========================================================
# HISTORY
# =========================================================

elif menu == "🕘 History":

    st.title("🕘 History")

    st.write(
        "Your previous study activity will appear here."
    )


# =========================================================
# SETTINGS
# =========================================================

elif menu == "⚙️ Settings":

    st.title("⚙️ Settings")

    st.write(
        "Application settings."
    )