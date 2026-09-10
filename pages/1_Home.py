import streamlit as st

st.set_page_config(
    page_title="Smart AI Study Assistant",
    page_icon="🎓",
    layout="wide"
)

# ================= HEADER =================

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

st.write("")

# ================= METRICS =================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🤖 AI Model", "Groq")

with col2:
    st.metric("📄 PDF", "Supported")

with col3:
    st.metric("🖼 OCR", "Enabled")

with col4:
    st.metric("🌍 Languages", "3")

st.divider()

# ================= FEATURES =================

st.subheader("✨ Key Features")

c1, c2 = st.columns(2)

with c1:

    st.success("""
### 📄 PDF Assistant

✅ Upload PDF

✅ AI Summary

✅ AI Quiz

✅ Ask Questions
""")

    st.info("""
### 💬 AI Chat

✅ Fast Groq AI

✅ Context Aware

✅ Student Friendly
""")

with c2:

    st.success("""
### 🖼 OCR Assistant

✅ Image to Text

✅ Explain Notes

✅ Generate Summary

✅ Quiz from Notes
""")

    st.info("""
### 🌍 Multilingual

✅ English

✅ Urdu

✅ Sindhi
""")

st.divider()

# ================= TECHNOLOGIES =================

st.subheader("🛠 Technologies Used")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.markdown("""
- Python
- Streamlit
- Groq API
""")

with tech2:
    st.markdown("""
- LangChain
- FAISS
- Sentence Transformers
""")

with tech3:
    st.markdown("""
- PDFPlumber
- EasyOCR
- Pillow
""")

st.divider()

# ================= WORKFLOW =================

st.subheader("🔄 AI Workflow")

st.markdown("""
1️⃣ Upload PDF

⬇

2️⃣ Extract Text

⬇

3️⃣ Create Chunks

⬇

4️⃣ Generate Embeddings

⬇

5️⃣ Store in FAISS

⬇

6️⃣ Retrieve Relevant Content

⬇

7️⃣ Generate AI Response using Groq
""")

st.divider()

st.success("🎯 Goal: Helping students learn faster with Artificial Intelligence.")

if st.button("🚀 Start Learning", use_container_width=True):
    st.balloons()
    st.success("Welcome! Use the left sidebar to explore the modules.")

st.divider()

st.markdown("""
<div style="text-align:center;color:gray;">
<h4>👩‍💻 Developed by SMIT Students</h4>

Smart AI Study Assistant • 2026

Powered by Groq AI
</div>
""", unsafe_allow_html=True)