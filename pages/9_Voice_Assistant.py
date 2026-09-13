import streamlit as st
st.title("🎤 Advanced Voice Assistant")

st.info(
    "Voice-based study interaction — currently under enhancement "
    "for broader cloud and browser compatibility."
)
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
from aiortc.contrib.media import MediaRecorder

from groq import Groq
from gtts import gTTS
from dotenv import load_dotenv

import os
import io
import tempfile
import time

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


# =========================================================
# PAGE
# =========================================================

st.title("🎤 Smart AI Voice Assistant")

st.write(
    "Ask your study question using your voice."
)

st.info(
    "🎙️ Click START → allow microphone access → "
    "speak your question → click STOP."
)


# =========================================================
# CREATE TEMP AUDIO FILE
# =========================================================

if "voice_file" not in st.session_state:

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_file.close()

    st.session_state.voice_file = temp_file.name


voice_file = st.session_state.voice_file


# =========================================================
# MICROPHONE
# =========================================================

st.write("### 🎙️ Record Your Question")


MEDIA_STREAM_CONSTRAINTS = {
    "video": False,
    "audio": {
        "echoCancellation": True,
        "noiseSuppression": True,
        "autoGainControl": True,
    },
}


def recorder_factory():

    return MediaRecorder(
        voice_file
    )


ctx = webrtc_streamer(

    key="smart-ai-voice-assistant",

    mode=WebRtcMode.SENDONLY,

    rtc_configuration={
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302"
                ]
            }
        ]
    },

    media_stream_constraints=MEDIA_STREAM_CONSTRAINTS,

    in_recorder_factory=recorder_factory,

    async_processing=True,
)


# =========================================================
# STATUS
# =========================================================

if ctx.state.playing:

    st.success(
        "🔴 Recording... Speak your question now."
    )

else:

    st.info(
        "🎙️ Click START to begin recording."
    )


# =========================================================
# PROCESS AFTER STOP
# =========================================================

if (
    not ctx.state.playing
    and os.path.exists(voice_file)
):

    file_size = os.path.getsize(voice_file)

    # Ignore empty/new file
    if file_size > 1000:

        st.success(
            "✅ Recording received!"
        )


        # =================================================
        # SHOW RECORDING
        # =================================================

        st.write("### 🎧 Your Recording")

        with open(
            voice_file,
            "rb"
        ) as audio_file:

            audio_bytes = audio_file.read()

        st.audio(
            audio_bytes,
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


                with open(
                    voice_file,
                    "rb"
                ) as audio_file:

                    result = client.audio.transcriptions.create(

                        file=(
                            "voice_question.wav",
                            audio_file.read(),
                            "audio/wav"
                        ),

                        model="whisper-large-v3",

                        language="en",

                        response_format="json",

                        temperature=0
                    )


                user_text = result.text.strip()


            except Exception as e:

                st.error(
                    f"Speech recognition error: {e}"
                )

                user_text = ""


        # =================================================
        # SHOW QUESTION
        # =================================================

        if user_text:

            st.write("### 🎤 You Said")

            st.success(
                user_text
            )


            # =================================================
            # AI ANSWER
            # =================================================

            with st.spinner(
                "🤖 AI is thinking..."
            ):

                try:

                    ai_response = ask_ai(
                        user_text,
                        language="English"
                    )

                except Exception as e:

                    ai_response = (
                        f"AI response error: {e}"
                    )


            st.write("### 🤖 AI Answer")

            st.write(
                ai_response
            )


            # =================================================
            # TEXT TO SPEECH
            # =================================================

            st.write(
                "### 🔊 AI Voice Answer"
            )

            with st.spinner(
                "🔊 Creating voice answer..."
            ):

                try:

                    tts = gTTS(
                        text=ai_response,
                        lang="en",
                        slow=False
                    )

                    audio_output = io.BytesIO()

                    tts.write_to_fp(
                        audio_output
                    )

                    audio_output.seek(0)

                    st.audio(
                        audio_output,
                        format="audio/mp3"
                    )

                except Exception as e:

                    st.error(
                        f"Voice output error: {e}"
                    )


        else:

            st.warning(
                "No speech was detected. "
                "Please click START and record your question again."
            )


# =========================================================
# CLEANUP
# =========================================================

if os.path.exists(voice_file):

    try:

        # Keep the file during the current page session.
        # It will be replaced when the page is refreshed.

        pass

    except Exception:

        pass

