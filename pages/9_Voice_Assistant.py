def recognize_audio(audio_file):
    """Convert recorded audio into text."""

    recognizer = sr.Recognizer()

    try:
        # Convert Streamlit audio to bytes
        audio_bytes = audio_file.getvalue()

        # Save audio temporarily
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
        st.warning("I could not understand the voice. Please speak clearly and try again.")
        return None

    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {e}")
        return None

    except Exception as e:
        st.error(f"Audio processing error: {e}")
        return None