"""
=========================================================
Smart AI Study Assistant
AI Chat Page

Modern ChatGPT Style UI

Features:
✔ AI Chat using Gemma (Ollama)
✔ Chat History
✔ English / Urdu / Sindhi Support
✔ Modern Interface
=========================================================
"""


# -----------------------------
# Imports
# -----------------------------

import streamlit as st
from utils.ai_engine import ask_ai



# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="wide"
)



# -----------------------------
# Custom CSS
# -----------------------------

st.markdown(
"""
<style>


/* Background */

.stApp{

background:
linear-gradient(
135deg,
#eef7ff,
#f5fbff
);

}



/* Header */

.ai-header{

background:
linear-gradient(
135deg,
#2563eb,
#06b6d4
);

padding:35px;

border-radius:25px;

color:white;

text-align:center;

box-shadow:
0px 10px 30px rgba(0,0,0,0.15);

}



.ai-header h1{

font-size:45px;

font-weight:800;

}



/* Chat messages */

[data-testid="stChatMessage"]{

background:white;

border-radius:20px;

padding:15px;

margin-bottom:15px;

box-shadow:
0px 5px 18px rgba(0,0,0,0.08);

}



/* Chat input */

[data-testid="stChatInput"]{

background:white;

border-radius:20px;

box-shadow:
0px 5px 20px rgba(0,0,0,0.1);

}



/* Select box */

.stSelectbox{

background:white;

border-radius:15px;

}



/* Button */

.stButton button{


background:
linear-gradient(
90deg,
#2563eb,
#06b6d4
);


color:white;

border-radius:20px;

border:none;

font-weight:bold;


}


.stButton button:hover{

transform:scale(1.05);

}



</style>

""",
unsafe_allow_html=True
)





# -----------------------------
# Header
# -----------------------------


st.markdown(
"""
<div class="ai-header">

<h1>
🤖 Smart AI Chat Assistant
</h1>

<p>
Your personal AI learning companion powered by Gemma
</p>

</div>

""",
unsafe_allow_html=True
)



st.write("")



# -----------------------------
# Language Selection
# -----------------------------


col1,col2 = st.columns([2,1])


with col1:

    language = st.selectbox(
        "🌍 Choose Response Language",
        [
            "English",
            "Urdu",
            "Sindhi"
        ]
    )



with col2:

    st.info(
        """
        🤖 AI Model  
        Gemma (Ollama)
        """
    )





st.divider()





# -----------------------------
# Chat History
# -----------------------------


if "messages" not in st.session_state:

    st.session_state.messages = []





# -----------------------------
# Clear Chat
# -----------------------------


if st.button("🗑 Clear Conversation"):

    st.session_state.messages = []

    st.success(
        "Chat history cleared!"
    )

    st.rerun()





# -----------------------------
# Display Chat
# -----------------------------


for message in st.session_state.messages:


    if message["role"]=="user":

        avatar="👩‍🎓"

    else:

        avatar="🤖"



    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(
            message["content"]
        )






# -----------------------------
# User Input
# -----------------------------


prompt = st.chat_input(
    "Ask anything about your studies..."
)





if prompt:



    # User message save

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )



    with st.chat_message(
        "user",
        avatar="👩‍🎓"
    ):

        st.markdown(prompt)




    # AI Response


    with st.chat_message(
        "assistant",
        avatar="🤖"
    ):


        with st.spinner(
            "🤖 AI is analyzing your question..."
        ):


            answer = ask_ai(
                prompt,
                language
            )


        st.markdown(
            answer
        )



    # Save AI response


    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )