import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

import os
import io
import wave
import queue
import threading
import av
import numpy as np

from utils.ai_engine import ask_ai


# =========================================================
# LOAD ENVIRONMENT
# =========================================================

load_dotenv()


# =========================================================
# GROQ CLIENT
# =========================================================

def get_groq_client():
    api_key = None

    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        pass

    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return None

    return Groq(api_key=api_key)


# =========================================================
# PAGE
# =========================================================

st.title("🎤 Smart AI Voice Assistant")

st.write(
    "Ask your study question using your voice."
)

st.info(
    "🎙️ Click START, allow microphone access, "
    "speak your question clearly, then click STOP."
)


# =========================================================
# TEXT TO SPEECH
# =========================================================

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


# =========================================================
# THREAD-SAFE AUDIO QUEUE
# =========================================================

audio_queue = queue.Queue()


# =========================================================
# AUDIO CALLBACK
# =========================================================

def audio_callback(frame: av.AudioFrame):

    try:
        audio = frame.to_ndarray()

        audio_queue.put(
            (
                audio.copy(),
                frame.sample_rate
            )
        )

    except Exception:
        pass

    return frame


# =========================================================
# MICROPHONE
# =========================================================

st.write("### 🎙️ Record Your Question")

ctx = webrtc_streamer(
    key="voice_assistant",

    mode=WebRtcMode.SENDONLY,

    audio_frame_callback=audio_callback,

    media_stream_constraints={
        "audio": {
            "echoCancellation": True,
            "noiseSuppression": True,
            "autoGainControl": True
        },
        "video": False
    },

    rtc_configuration={
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302"
                ]
            }
        ]
    },

    async_processing=True
)


# =========================================================
# PROCESS AFTER RECORDING
# =========================================================

if not ctx.state.playing:

    collected_audio = []

    sample_rate = None

    while not audio_queue.empty():

        try:
            audio, rate = audio_queue.get_nowait()

            collected_audio.append(audio)

            if rate:
                sample_rate = rate

        except queue.Empty:
            break


    # =====================================================
    # NO AUDIO
    # =====================================================

    if not collected_audio:

        st.info(
            "🎙️ Click START and speak your question."
        )

    else:

        st.success(
            "✅ Recording received!"
        )


        # =================================================
        # COMBINE AUDIO FRAMES
        # =================================================

        try:

            audio_data = np.concatenate(
                collected_audio,
                axis=1
            )

        except Exception:

            st.error(
                "Could not combine microphone audio."
            )

            st.stop()


        # =================================================
        # CONVERT TO MONO
        # =================================================

        if audio_data.ndim > 1:

            if audio_data.shape[0] > 1:

                audio_data = np.mean(
                    audio_data,
                    axis=0
                )

            else:

                audio_data = audio_data[0]


        # =================================================
        # NORMALIZE AUDIO
        # =================================================

        audio_data = audio_data.astype(
            np.float32
        )

        max_value = np.max(
            np.abs(audio_data)
        )

        if max_value > 0:

            audio_data = (
                audio_data / max_value
            ) * 32767


        audio_data = np.clip(
            audio_data,
            -32768,
            32767
        ).astype(np.int16)


        # =================================================
        # SAMPLE RATE
        # =================================================

        if not sample_rate:

            sample_rate = 48000


        # =================================================
        # CREATE WAV
        # =================================================

        wav_buffer = io.BytesIO()

        with wave.open(
            wav_buffer,
            "wb"
        ) as wav_file:

            wav_file.setnchannels(1)

            wav_file.setsampwidth(2)

            wav_file.setframerate(
                sample_rate
            )

            wav_file.writeframes(
                audio_data.tobytes()
            )


        wav_buffer.seek(0)

        wav_bytes = wav_buffer.getvalue()


        # =================================================
        # SHOW RECORDING
        # =================================================

        st.write("### 🎧 Your Recording")

        st.audio(
            wav_bytes,
            format="audio/wav"
        )


        # =================================================
        # SPEECH TO TEXT
        # =================================================

        with st.spinner(
            "🎧 Converting your voice to text..."
        ):

            try:

                client = get_groq_client()

                if client is None:

                    st.error(
                        "GROQ_API_KEY is missing. "
                        "Please add GROQ_API_KEY "
                        "to Streamlit Secrets."
                    )

                    st.stop()


                result = client.audio.transcriptions.create(

                    file=(
                        "voice_question.wav",
                        wav_bytes,
                        "audio/wav"
                    ),

                    model="whisper-large-v3",

                    language="en",

                    response_format="json",

                    temperature=0
                )


                user_text = (
                    result.text.strip()
                )


            except Exception as e:

                st.error(
                    f"Speech recognition error: {e}"
                )

                user_text = ""


        # =================================================
        # SHOW TRANSCRIPTION
        # =================================================

        if user_text:

            st.write("### 🎤 You Said")

            st.success(
                user_text
            )


            # =============================================
            # AI ANSWER
            # =============================================

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


            # =============================================
            # VOICE ANSWER
            # =============================================

            st.write(
                "### 🔊 AI Voice Answer"
            )

            speak(
                ai_response
            )


        else:

            st.warning(
                "No speech was detected. "
                "Please record your question again."
            )