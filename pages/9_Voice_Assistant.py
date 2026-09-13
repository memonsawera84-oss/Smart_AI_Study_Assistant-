import streamlit as st
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

import os
import io
import wave

from st_audiorec import st_audiorec

from utils.ai_engine import ask_ai


# ==========================================
# LOAD ENVIRONMENT
# ==========================================

load_dotenv()


# ==========================================
# GROQ CLIENT
# ==========================================

def get_groq_client():

    api_key = None

    # Streamlit Cloud Secrets
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


# ==========================================
# PAGE
# ==========================================

st.title("🎤 Smart AI Voice Assistant")

st.write(
    "Ask your question using your voice."
)

st.info(
    "🎙️ Click START, allow microphone access, "
    "speak your question, then click STOP."
)


# ==========================================
# TEXT TO SPEECH
# ==========================================

def speak(text):

    try:

        tts = gTTS(
            text=text,
            lang="en",
            slow=False
        )

        audio_buffer = io.BytesIO()

        tts.write_to_fp(audio_buffer)

        audio_buffer.seek(0)

        st.audio(
            audio_buffer,
            format="audio/mp3"
        )

    except Exception as e:

        st.error(
            f"Voice output error: {e}"
        )


# ==========================================
# AUDIO VALIDATION
# ==========================================

def validate_audio(audio_bytes):

    try:

        with wave.open(
            io.BytesIO(audio_bytes),
            "rb"
        ) as wav:

            sample_rate = wav.getframerate()
            frames = wav.getnframes()
            channels = wav.getnchannels()

            duration = frames / float(sample_rate)

            return {
                "sample_rate": sample_rate,
                "frames": frames,
                "channels": channels,
                "duration": duration
            }

    except Exception as e:

        st.error(
            f"Audio validation error: {e}"
        )

        return None


# ==========================================
# SPEECH TO TEXT
# ==========================================

def recognize_audio(audio_bytes):

    client = get_groq_client()

    if client is None:

        st.error(
            "GROQ_API_KEY is missing. "
            "Please add it to Streamlit Secrets."
        )

        return None

    try:

        if not audio_bytes:

            st.warning(
                "No audio was recorded."
            )

            return None

        # ----------------------------------
        # Validate WAV
        # ----------------------------------

        info = validate_audio(audio_bytes)

        if info is None:
            return None

        duration = info["duration"]

        if duration < 0.8:

            st.warning(
                "Recording is too short. "
                "Please speak for at least 1 second."
            )

            return None

        if duration > 60:

            st.warning(
                "Recording is too long. "
                "Please keep your question under 60 seconds."
            )

            return None

        # ----------------------------------
        # GROQ WHISPER
        # ----------------------------------

        transcription = client.audio.transcriptions.create(

            file=(
                "voice_question.wav",
                audio_bytes,
                "audio/wav"
            ),

            model="whisper-large-v3",

            language="en",

            prompt=(
                "This is an English question from a student "
                "using an AI study assistant. "
                "Transcribe exactly what the student says."
            ),

            response_format="json",

            temperature=0.0
        )

        text = transcription.text.strip()

        if not text:

            st.warning(
                "I could not detect speech. "
                "Please speak clearly and try again."
            )

            return None

        return text

    except Exception as e:

        st.error(
            f"Speech recognition error: {e}"
        )

        return None


# ==========================================
# BROWSER MICROPHONE RECORDER
# ==========================================

st.write("### 🎙️ Record Your Question")

audio_data = st_audiorec()


# ==========================================
# PROCESS RECORDING
# ==========================================

if audio_data:

    st.success(
        "✅ Recording received successfully!"
    )

    # --------------------------------------
    # PLAY USER RECORDING
    # --------------------------------------

    st.write("### 🎧 Your Recording")

    st.audio(
        audio_data,
        format="audio/wav"
    )

    # --------------------------------------
    # SPEECH TO TEXT
    # --------------------------------------

    with st.spinner(
        "🎧 Converting your voice to text..."
    ):

        user_text = recognize_audio(
            audio_data
        )

    # --------------------------------------
    # SHOW TRANSCRIPT
    # --------------------------------------

    if user_text:

        st.write("### 🎤 You Said")

        st.success(user_text)

        # ----------------------------------
        # AI RESPONSE
        # ----------------------------------

        with st.spinner(
            "🤖 AI is thinking..."
        ):

            ai_response = ask_ai(
                user_text,
                language="English"
            )

        # ----------------------------------
        # SHOW AI RESPONSE
        # ----------------------------------

        st.write("### 🤖 AI Answer")

        st.write(ai_response)

        # ----------------------------------
        # AI VOICE
        # ----------------------------------

        st.write("### 🔊 AI Voice Answer")

        speak(ai_response)

    else:

        st.warning(
            "Please record your question again "
            "and speak clearly into the microphone."
        )