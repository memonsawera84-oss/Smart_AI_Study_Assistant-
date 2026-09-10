import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile

from utils.ai_engine import ask_ai


st.title("🎤 Smart AI Voice Assistant")

st.write("Ask your question using your voice.")


def speak(text):
    """Convert AI response to speech."""

    try:
        tts = gTTS(text=text, lang="en")

        temp = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        )

        tts.save(temp.name)

        st.audio(temp.name, format="audio/mp3")

    except Exception as e:
        st.error(f"Voice output error: {e}")


def recognize_audio(audio_file):
    """Convert uploaded/recorded audio into text."""

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio)

        return text

    except sr.UnknownValueError:
        return None

    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {e}")
        return None

    except Exception as e:
        st.error(f"Audio processing error: {e}")
        return None


audio_file = st.audio_input("🎤 Record your question")

if audio_file:

    st.audio(audio_file)

    with st.spinner("🎧 Understanding your question..."):

        user_text = recognize_audio(audio_file)

    if user_text:

        st.write("### 🎤 You")
        st.write(user_text)

        with st.spinner("🤖 AI is thinking..."):

            ai_response = ask_ai(user_text)

        st.write("### 🤖 AI")
        st.write(ai_response)

        speak(ai_response)

    else:

        st.error("Sorry, your voice could not be recognized.")