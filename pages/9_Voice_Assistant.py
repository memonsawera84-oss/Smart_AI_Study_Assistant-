import streamlit as st
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

import os
import io
import wave
import numpy as np

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
    "🎙️ Click the microphone button, "
    "speak your question clearly, then stop recording."
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
# AUDIO ANALYSIS
# ==========================================

def analyze_audio(audio_bytes):

    try:

        wav_buffer = io.BytesIO(audio_bytes)

        with wave.open(wav_buffer, "rb") as wav:

            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frames = wav.getnframes()

            duration = frames / float(sample_rate)

            raw_audio = wav.readframes(frames)

        # ----------------------------------
        # Calculate audio volume
        # ----------------------------------

        rms = 0

        if sample_width == 2:

            samples = np.frombuffer(
                raw_audio,
                dtype=np.int16
            )

            if len(samples) > 0:

                rms = float(
                    np.sqrt(
                        np.mean(
                            samples.astype(np.float64) ** 2
                        )
                    )
                )

        return {
            "channels": channels,
            "sample_width": sample_width,
            "sample_rate": sample_rate,
            "frames": frames,
            "duration": duration,
            "rms": rms
        }

    except Exception as e:

        st.error(
            f"Audio validation error: {e}"
        )

        return None


# ==========================================
# SPEECH TO TEXT
# ==========================================

def recognize_audio(audio_file):

    client = get_groq_client()

    if client is None:

        st.error(
            "GROQ_API_KEY is missing. "
            "Please add it to Streamlit Secrets."
        )

        return None

    try:

        # ----------------------------------
        # Get complete WAV bytes
        # ----------------------------------

        audio_bytes = audio_file.getvalue()

        if not audio_bytes:

            st.warning(
                "No audio was recorded."
            )

            return None

        # ----------------------------------
        # Analyze recording
        # ----------------------------------

        info = analyze_audio(audio_bytes)

        if info is None:
            return None

        duration = info["duration"]
        rms = info["rms"]

        # ----------------------------------
        # Recording too short
        # ----------------------------------

        if duration < 0.8:

            st.warning(
                "Recording is too short. "
                "Please speak for at least 1 second."
            )

            return None

        # ----------------------------------
        # Recording too long
        # ----------------------------------

        if duration > 60:

            st.warning(
                "Recording is too long. "
                "Please keep your question under 60 seconds."
            )

            return None

        # ----------------------------------
        # Detect silent microphone
        # ----------------------------------

        if rms < 150:

            st.error(
                "⚠️ The Cloud app received almost silent audio. "
                "Please allow microphone access in your browser "
                "and try again."
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
                "This is a student's English study question "
                "for an AI study assistant. "
                "Transcribe exactly what the student says."
            ),

            response_format="json",

            temperature=0.0
        )

        # ----------------------------------
        # Extract transcription
        # ----------------------------------

        text = transcription.text.strip()

        if not text:

            st.warning(
                "No speech was detected. "
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
# MICROPHONE
# ==========================================

audio_file = st.audio_input(

    "🎤 Record your question",

    sample_rate=16000,

    key="voice_question"
)


# ==========================================
# PROCESS RECORDING
# ==========================================

if audio_file:

    st.success(
        "✅ Recording received!"
    )

    # --------------------------------------
    # Play EXACT recording received by Cloud
    # --------------------------------------

    st.write("### 🎧 Your Recording")

    st.audio(
        audio_file,
        format="audio/wav"
    )

    # --------------------------------------
    # Speech recognition
    # --------------------------------------

    with st.spinner(
        "🎧 Converting your voice to text..."
    ):

        user_text = recognize_audio(
            audio_file
        )

    # --------------------------------------
    # AI RESPONSE
    # --------------------------------------

    if user_text:

        st.write("### 🎤 You")

        st.success(user_text)

        with st.spinner(
            "🤖 AI is thinking..."
        ):

            ai_response = ask_ai(
                user_text,
                language="English"
            )

        st.write("### 🤖 AI")

        st.write(ai_response)

        # ----------------------------------
        # AI VOICE
        # ----------------------------------

        st.write("### 🔊 AI Voice")

        speak(ai_response)

    else:

        st.warning(
            "Please record your question again "
            "and speak clearly into your microphone."
        )