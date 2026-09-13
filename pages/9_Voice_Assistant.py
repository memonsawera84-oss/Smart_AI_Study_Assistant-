python
import streamlit as st
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

import os
import io
import wave
import numpy as np

from st_audiorec import st_audiorec
from utils.ai_engine import ask_ai


# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------
load_dotenv()


# ---------------------------------------------------------
# Groq Client
# ---------------------------------------------------------
def get_groq_client():
    api_key = None

    # Streamlit Cloud Secrets
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    # Local .env fallback
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


# ---------------------------------------------------------
# Page UI
# ---------------------------------------------------------
st.title("🎤 Smart AI Voice Assistant")

st.write(
    "Ask your question using your voice."
)

st.info(
    "🎙️ Click START, allow microphone access, speak your question, "
    "then click STOP."
)


# ---------------------------------------------------------
# Text to Speech
# ---------------------------------------------------------
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
        st.error(f"Voice output error: {e}")


# ---------------------------------------------------------
# Convert audio to 16 kHz Mono WAV
# ---------------------------------------------------------
def normalize_audio(audio_bytes):
    try:
        input_buffer = io.BytesIO(audio_bytes)

        with wave.open(input_buffer, "rb") as wav:

            channels = wav.getnchannels()
            sample_width = wav.getsampwidth()
            original_rate = wav.getframerate()
            frames = wav.getnframes()

            raw_audio = wav.readframes(frames)

        # We expect 16-bit audio
        if sample_width != 2:
            st.error(
                f"Unsupported audio sample width: {sample_width}"
            )
            return None

        # Convert raw bytes to int16
        samples = np.frombuffer(
            raw_audio,
            dtype=np.int16
        )

        if len(samples) == 0:
            st.error("No audio samples were recorded.")
            return None

        # -------------------------------------------------
        # Stereo -> Mono
        # -------------------------------------------------
        if channels > 1:

            usable_length = (
                len(samples) // channels
            ) * channels

            samples = samples[:usable_length]

            samples = samples.reshape(
                -1,
                channels
            )

            samples = samples.mean(
                axis=1
            )

        samples = samples.astype(
            np.float32
        )

        # -------------------------------------------------
        # Resample -> 16000 Hz
        # -------------------------------------------------
        target_rate = 16000

        if original_rate != target_rate:

            original_length = len(samples)

            new_length = int(
                original_length
                * target_rate
                / original_rate
            )

            if new_length <= 0:
                st.error(
                    "Audio is too short to process."
                )
                return None

            old_positions = np.linspace(
                0,
                1,
                original_length
            )

            new_positions = np.linspace(
                0,
                1,
                new_length
            )

            samples = np.interp(
                new_positions,
                old_positions,
                samples
            )

        # -------------------------------------------------
        # Convert back to 16-bit PCM
        # -------------------------------------------------
        samples = np.clip(
            samples,
            -32768,
            32767
        ).astype(np.int16)

        # -------------------------------------------------
        # Create new WAV
        # -------------------------------------------------
        output_buffer = io.BytesIO()

        with wave.open(
            output_buffer,
            "wb"
        ) as output_wav:

            output_wav.setnchannels(1)
            output_wav.setsampwidth(2)
            output_wav.setframerate(16000)

            output_wav.writeframes(
                samples.tobytes()
            )

        output_buffer.seek(0)

        return output_buffer.getvalue()

    except Exception as e:

        st.error(
            f"Audio conversion error: {e}"
        )

        return None


# ---------------------------------------------------------
# Speech Recognition using Groq Whisper
# ---------------------------------------------------------
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

        # Convert recorder audio to
        # 16 kHz mono WAV
        normalized_audio = normalize_audio(
            audio_bytes
        )

        if normalized_audio is None:
            return None

        # -------------------------------------------------
        # Check duration
        # -------------------------------------------------
        with wave.open(
            io.BytesIO(normalized_audio),
            "rb"
        ) as wav:

            frames = wav.getnframes()
            rate = wav.getframerate()

            duration = frames / float(rate)

            raw_audio = wav.readframes(frames)

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

        # -------------------------------------------------
        # Check that audio actually contains sound
        # -------------------------------------------------
        samples = np.frombuffer(
            raw_audio,
            dtype=np.int16
        )

        if len(samples) > 0:

            rms = float(
                np.sqrt(
                    np.mean(
                        samples.astype(
                            np.float64
                        ) ** 2
                    )
                )
            )

            if rms < 50:

                st.error(
                    "⚠️ Very little sound was detected. "
                    "Please speak closer to your microphone "
                    "and try again."
                )

                return None

        # -------------------------------------------------
        # Send ACTUAL normalized audio to Whisper
        # -------------------------------------------------
        transcription = (
            client.audio.transcriptions.create(

                file=(
                    "voice_question.wav",
                    normalized_audio,
                    "audio/wav"
                ),

                model="whisper-large-v3",

                language="en",

                response_format="json",

                temperature=0.0
            )
        )

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


# ---------------------------------------------------------
# Voice Recorder
# ---------------------------------------------------------
st.write("### 🎙️ Record Your Question")

audio_data = st_audiorec()


# ---------------------------------------------------------
# Process Recording
# ---------------------------------------------------------
if audio_data:

    st.success(
        "✅ Recording received successfully!"
    )

    st.write("### 🎧 Your Recording")

    st.audio(
        audio_data,
        format="audio/wav"
    )

    # -----------------------------------------------------
    # Convert Speech -> Text
    # -----------------------------------------------------
    with st.spinner(
        "🎧 Converting your voice to text..."
    ):

        user_text = recognize_audio(
            audio_data
        )

    # -----------------------------------------------------
    # Display User Question
    # -----------------------------------------------------
    if user_text:

        st.write("### 🎤 You Said")

        st.success(
            user_text
        )

        # -------------------------------------------------
        # AI Answer
        # -------------------------------------------------
        with st.spinner(
            "🤖 AI is thinking..."
        ):

            ai_response = ask_ai(
                user_text,
                language="English"
            )

        st.write("### 🤖 AI Answer")

        st.write(
            ai_response
        )

        # -------------------------------------------------
        # Voice Answer
        # -------------------------------------------------
        st.write(
            "### 🔊 AI Voice Answer"
        )

        speak(
            ai_response
        )

    else:

        st.warning(
            "Please record your question again "
            "and speak clearly into the microphone."
        )

