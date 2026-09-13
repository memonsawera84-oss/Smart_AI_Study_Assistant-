import streamlit as st
from groq import Groq
from gtts import gTTS
import tempfile
import os

from utils.ai_engine import ask_ai


# ==============================
# GROQ CLIENT
# ==============================

def get_groq_client():
    """Create Groq client using Streamlit Cloud Secrets or local .env."""

    api_key = None

    # Streamlit Cloud
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    # Local .env
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


# ==============================
# PAGE TITLE
# ==============================

st.title("🎤 Smart AI Voice Assistant")

st.write("Ask your question using your voice.")

st.info("🎙️ Click the microphone button below and speak clearly.")


# ==============================
# TEXT TO SPEECH
# ==============================

def speak(text):
    """Convert AI response into speech."""

    try:
        tts = gTTS(
            text=text,
            lang="en"
        )

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp.name)

        st.audio(
            temp.name,
            format="audio/mp3"
        )

    except Exception as e:
        st.error(f"Voice output error: {e}")


# ==============================
# SPEECH TO TEXT
# ==============================

def recognize_audio(audio_file):
    """Convert recorded voice to text using Groq Whisper."""

    client = get_groq_client()

    if client is None:
        st.error(
            "GROQ_API_KEY is not configured. "
            "Please add it to Streamlit Secrets."
        )
        return None

    try:

        # Get recorded WAV bytes
        audio_bytes = audio_file.getvalue()

        # Send audio directly to Groq Whisper
        transcription = client.audio.transcriptions.create(
            file=(
                "voice_question.wav",
                audio_bytes
            ),
            model="whisper-large-v3-turbo",
            language="en",
            response_format="json",
            temperature=0.0
        )

        text = transcription.text.strip()

        if text:
            return text

        st.warning(
            "No speech was detected. Please speak clearly and try again."
        )

        return None

    except Exception as e:

        st.error(
            f"Speech recognition error: {e}"
        )

        return None


# ==============================
# MICROPHONE
# ==============================

audio_file = st.audio_input(
    "🎤 Record your question",
    sample_rate=16000
)


# ==============================
# PROCESS VOICE
# ==============================

if audio_file:

    st.success("✅ Recording received!")

    st.audio(audio_file)

    with st.spinner("🎧 Converting your voice to text..."):

        user_text = recognize_audio(audio_file)


    # ==============================
    # USER QUESTION
    # ==============================

    if user_text:

        st.write("### 🎤 You")
        st.write(user_text)


        # ==============================
        # AI RESPONSE
        # ==============================

        with st.spinner("🤖 AI is thinking..."):

            ai_response = ask_ai(user_text)


        st.write("### 🤖 AI")
        st.write(ai_response)


        # ==============================
        # AI VOICE
        # ==============================

        st.write("### 🔊 AI Voice")

        speak(ai_response)

    else:

        st.warning(
            "Please try recording again and speak clearly."
        )