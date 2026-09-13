import streamlit as st
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv
import os
import io
import wave

from utils.ai_engine import ask_ai


# ==========================================
# LOAD LOCAL ENVIRONMENT
# ==========================================

load_dotenv()


# ==========================================
# GROQ CLIENT
# ==========================================

def get_groq_client():
    """Create Groq client from Streamlit Secrets or local .env."""

    api_key = None

    # Streamlit Cloud
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    # Local environment
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


# ==========================================
# PAGE
# ==========================================

st.title("🎤 Smart AI Voice Assistant")

st.write("Ask your question using your voice.")

st.info(
    "🎙️ Click the microphone button, speak your question clearly, "
    "then stop recording."
)


# ==========================================
# TEXT TO SPEECH
# ==========================================

def speak(text):
    """Convert AI response to spoken English."""

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
        st.error(f"Voice output error: {e}")


# ==========================================
# VALIDATE WAV
# ==========================================

def validate_audio(audio_bytes):
    """Check whether Streamlit microphone produced a valid WAV."""

    try:
        with wave.open(io.BytesIO(audio_bytes), "rb") as wav:

            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            sample_rate = wav.getframerate()
            frames = wav.getnframes()

            duration = frames / float(sample_rate)

            return {
                "channels": channels,
                "sample_width": sample_width,
                "sample_rate": sample_rate,
                "frames": frames,
                "duration": duration
            }

    except Exception as e:
        st.error(f"Invalid audio recording: {e}")
        return None


# ==========================================
# SPEECH TO TEXT
# ==========================================

def recognize_audio(audio_file):

    client = get_groq_client()

    if client is None:
        st.error(
            "GROQ_API_KEY is not configured. "
            "Please add GROQ_API_KEY to Streamlit Secrets."
        )
        return None

    try:

        # --------------------------------------
        # Read microphone recording
        # --------------------------------------

        audio_bytes = audio_file.getvalue()

        if not audio_bytes:
            st.warning("No audio was recorded.")
            return None

        # --------------------------------------
        # Validate WAV
        # --------------------------------------

        info = validate_audio(audio_bytes)

        if info is None:
            return None

        # --------------------------------------
        # Check recording duration
        # --------------------------------------

        if info["duration"] < 0.7:

            st.warning(
                "Recording is too short. "
                "Please speak for at least one second."
            )

            return None

        if info["duration"] > 60:

            st.warning(
                "Recording is too long. "
                "Please keep your question under 60 seconds."
            )

            return None

        # --------------------------------------
        # Send WAV to Groq Whisper
        # --------------------------------------

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

        # --------------------------------------
        # Get text
        # --------------------------------------

        text = transcription.text.strip()

        if not text:

            st.warning(
                "I could not detect any speech. "
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
    sample_rate=16000
)


# ==========================================
# PROCESS RECORDING
# ==========================================

if audio_file:

    st.success("✅ Recording received!")

    # Show recorded audio
    st.audio(audio_file)

    # --------------------------------------
    # Speech to Text
    # --------------------------------------

    with st.spinner(
        "🎧 Listening and converting your voice to text..."
    ):

        user_text = recognize_audio(audio_file)

    # --------------------------------------
    # If speech detected
    # --------------------------------------

    if user_text:

        st.write("### 🎤 You")
        st.write(user_text)

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