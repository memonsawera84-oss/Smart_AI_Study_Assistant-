import streamlit as st

from utils.ai_engine import ask_ai



st.set_page_config(
    page_title="AI Summarizer",
    page_icon="📝",
    layout="wide"
)



st.title("📝 Smart AI Summarizer")


st.write(
"Generate smart summaries from your notes using AI."
)


st.divider()



notes = st.text_area(
    "📚 Enter your notes",
    height=250
)



language = st.selectbox(
    "🌍 Language",
    [
        "English",
        "Urdu",
        "Sindhi"
    ]
)



if st.button(
    "✨ Generate Summary"
):


    if notes:


        with st.spinner(
            "🤖 AI is summarizing..."
        ):


            prompt = f"""

            Summarize the following study notes.

            Give important points,
            simple explanation,
            and key concepts.

            Notes:

            {notes}

            """


            summary = ask_ai(
                prompt,
                language
            )


        st.success(
            "Summary Generated!"
        )


        st.markdown(
            summary
        )


    else:

        st.warning(
            "Please enter notes."
        )