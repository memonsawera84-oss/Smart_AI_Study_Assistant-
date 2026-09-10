import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile

from utils.ai_engine import ask_ai


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
    """Convert recorded audio into text."""

    recognizer = sr.Recognizer()

    try:

        # Get recorded audio bytes
        audio_bytes = audio_file.getvalue()

        # Save recording as WAV file
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
        ) as temp_audio:

            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name

        # Read WAV file
        with sr.AudioFile(temp_audio_path) as source:

            audio = recognizer.record(source)

        # Convert speech to text
        text = recognizer.recognize_google(
            audio,
            language="en-US"
        )

        return text

    except sr.UnknownValueError:

        st.warning(
            "I could not understand your voice. "
            "Please speak clearly and try again."
        )

        return None

    except sr.RequestError as e:

        st.error(
            f"Speech recognition service error: {e}"
        )

        return None

    except Exception as e:

        st.error(
            f"Audio processing error: {e}"
        )

        return None


# ==============================
# MICROPHONE
# ==============================

audio_file = st.audio_input(
    "🎤 Record your question"
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