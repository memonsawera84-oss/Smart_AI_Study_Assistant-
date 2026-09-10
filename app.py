import streamlit as st


# ==============================
# PAGE CONFIGURATION
# ==============================

st.set_page_config(
    page_title="Smart AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)



# ==============================
# CUSTOM CSS
# ==============================

st.markdown("""
<style>


/* ---------- Main Background ---------- */

.stApp {

    background:
    linear-gradient(
        135deg,
        #eef6ff,
        #f8fbff,
        #e8f4ff
    );

}



/* ---------- Sidebar ---------- */


[data-testid="stSidebar"] {

    background:
    linear-gradient(
        180deg,
        #1e3c72,
        #2a5298
    );

}


[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {

    color:white !important;

}



/* ---------- Hero Section ---------- */


.hero {


padding:45px;


border-radius:25px;


background:

linear-gradient(
135deg,
#2563eb,
#06b6d4
);



color:white;


text-align:center;


box-shadow:

0px 10px 30px rgba(0,0,0,0.25);


}




.hero-title {


font-size:45px;


font-weight:800;


color:white;


animation:glow 2s infinite alternate;


}




@keyframes glow {


from {

text-shadow:
0 0 10px #ffffff;

}


to {

text-shadow:
0 0 30px #06b6d4;

}


}





/* ---------- Feature Cards ---------- */


.card {


background:

rgba(255,255,255,0.75);



padding:25px;



height:180px;



border-radius:20px;



text-align:center;



box-shadow:

0px 8px 25px rgba(0,0,0,0.10);



transition:0.4s;



backdrop-filter:blur(10px);



}




.card h2 {


font-size:35px;


}




.card h3 {


color:#2563eb;


}



.card p {


color:#1f2937;


font-size:16px;


}




.card:hover {


transform:

translateY(-8px);



box-shadow:

0px 15px 35px rgba(0,0,0,0.20);


}





/* ---------- Metrics ---------- */


[data-testid="stMetric"] {


background:

rgba(255,255,255,0.70);



padding:20px;



border-radius:18px;



box-shadow:

0px 5px 20px rgba(0,0,0,0.10);



}




/* ---------- Buttons ---------- */


.stButton button {


background:

linear-gradient(
90deg,
#2563eb,
#06b6d4
);



color:white;



border-radius:20px;



border:none;



padding:10px 25px;



font-size:18px;



font-weight:bold;



}



.stButton button:hover {


transform:scale(1.05);


}





/* ---------- About Section ---------- */


.about-box {


background:

rgba(255,255,255,0.75);



padding:30px;



border-radius:20px;



box-shadow:

0px 8px 25px rgba(0,0,0,0.10);



}



.about-box h2 {


color:#2563eb;


}



.about-box p,
.about-box li {


color:#1f2937;



font-size:17px;



line-height:1.8;



}





/* ---------- Dark Mode Support ---------- */


@media (prefers-color-scheme: dark) {



.stApp {


background:

linear-gradient(
135deg,
#0f172a,
#1e293b
);


}



.card,
.about-box,
[data-testid="stMetric"] {


background:

rgba(30,41,59,0.90);


}




.card h3,
.card p,
.about-box h2,
.about-box p,
.about-box li {


color:white !important;


}



}





</style>

""", unsafe_allow_html=True)





# ==============================
# SIDEBAR
# ==============================


st.sidebar.title(
"🎓 Smart AI Study Assistant"
)


st.sidebar.markdown("---")



st.sidebar.success(
"👋 Welcome Student!"
)



menu = st.sidebar.radio(
"Navigation",
[
"🏠 Home",
"💬 AI Chat",
"📄 PDF Assistant",
"📝 Summarizer",
"❓ Quiz Generator",
"🖼 OCR",
"📚 History",
"⚙ Settings"
]
)



st.sidebar.markdown("---")



st.sidebar.info(
"🚀 Powered by Python + Streamlit + AI"
)
# ==============================
# HOME PAGE
# ==============================


if menu == "🏠 Home":



    # ---------- Hero Banner ----------


    st.markdown("""

    <div class="hero">


    <div class="hero-title">

    🎓 Smart AI Study Assistant

    </div>


    <h3>
    Your Personal AI Learning Companion
    </h3>


    <p>

    Learn smarter with AI-powered PDF analysis,
    summarization, quizzes and intelligent chat.

    </p>


    </div>

    """, unsafe_allow_html=True)




    st.write("")




    # ---------- Metrics ----------


    c1,c2,c3,c4 = st.columns(4)



    with c1:

        st.metric(
            "📄 PDFs Uploaded",
            "0"
        )



    with c2:

        st.metric(
            "📝 Summaries",
            "0"
        )



    with c3:

        st.metric(
            "❓ Quizzes",
            "0"
        )



    with c4:

        st.metric(
            "💬 AI Chats",
            "0"
        )





    st.divider()





    # ---------- Features ----------


    st.header(
        "🚀 AI Features"
    )




    # First Row


    col1,col2,col3 = st.columns(3)



    with col1:

        st.markdown("""
        <div class="card">

        <h2>📄</h2>

        <h3>PDF Assistant</h3>

        <p>
        Upload PDFs and get AI explanations.
        </p>

        </div>

        """,
        unsafe_allow_html=True)





    with col2:

        st.markdown("""
        <div class="card">

        <h2>📝</h2>

        <h3>Smart Summarizer</h3>

        <p>
        Convert long notes into short summaries.
        </p>

        </div>

        """,
        unsafe_allow_html=True)





    with col3:

        st.markdown("""
        <div class="card">

        <h2>❓</h2>

        <h3>Quiz Generator</h3>

        <p>
        Generate AI based MCQs and quizzes.
        </p>

        </div>

        """,
        unsafe_allow_html=True)






    st.write("")





    # Second Row


    col4,col5,col6 = st.columns(3)




    with col4:


        st.markdown("""
        <div class="card">


        <h2>💬</h2>


        <h3>AI Chat</h3>


        <p>
        Ask questions and learn with AI.
        </p>


        </div>

        """,
        unsafe_allow_html=True)






    with col5:


        st.markdown("""
        <div class="card">


        <h2>🖼</h2>


        <h3>OCR Reader</h3>


        <p>
        Extract text from images and notes.
        </p>


        </div>

        """,
        unsafe_allow_html=True)







    with col6:


        st.markdown("""
        <div class="card">


        <h2>🔊</h2>


        <h3>Voice Assistant</h3>


        <p>
        Voice-based AI learning support.
        </p>


        </div>

        """,
        unsafe_allow_html=True)





    st.divider()





    # ---------- About Project ----------



    st.markdown("""
    
    <div class="about-box">


    <h2>
    📌 About Project
    </h2>



    <p>
    Smart AI Study Assistant is a multimodal AI learning platform designed for students.
    </p>



    <p>
    It helps students:
    </p>



    <ul>

    <li>✔ Understand PDFs using AI</li>

    <li>✔ Summarize study notes</li>

    <li>✔ Generate MCQs automatically</li>

    <li>✔ Extract text from images using OCR</li>

    <li>✔ Chat with AI assistant</li>

    <li>✔ Learn efficiently with smart tools</li>


    </ul>



    <p>
    🚀 Built using AI, RAG, OCR and Streamlit.
    </p>



    </div>


    """,
    unsafe_allow_html=True)





    st.divider()





    # ---------- Start Button ----------


    if st.button(
        "🚀 Start Learning"
    ):


        st.balloons()


        st.success(
            "AI Learning Journey Started!"
        )





    st.caption(
        "© 2026 Smart AI Study Assistant | AI Powered Learning Platform"
    )