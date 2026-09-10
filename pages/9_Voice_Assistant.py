import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import tempfile

from utils.ai_engine import ask_ai

st.title("🎤 Smart AI Voice Assistant")


def speak(text):
    tts = gTTS(text=text, lang="en")

    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp.name)

    st.audio(temp.name, format="audio/mp3", autoplay=True)


def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        st.info("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:
        return recognizer.recognize_google(audio)

    except:
        return None


if st.button("🎤 Start Listening"):

    user_text = listen()

    if user_text:

        st.write("### 🎤 You")
        st.write(user_text)

        ai_response = ask_ai(user_text)

        st.write("### 🤖 AI")
        st.write(ai_response)

        speak(ai_response)

    else:

        st.error("Voice not recognized.")