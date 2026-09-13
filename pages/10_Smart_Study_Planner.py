import streamlit as st
from datetime import date, timedelta
from utils.ai_engine import ask_ai


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="🧠",
    layout="wide"
)


# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------

if "study_plan" not in st.session_state:
    st.session_state.study_plan = ""

if "study_topics" not in st.session_state:
    st.session_state.study_topics = []

if "completed_topics" not in st.session_state:
    st.session_state.completed_topics = set()

if "planner_generated" not in st.session_state:
    st.session_state.planner_generated = False


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🧠 Smart Study Planner")

st.markdown(
    """
    Create a personalized AI-powered study plan based on your
    subjects, available study time, difficulty level, and exam date.
    """
)

st.divider()


# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    subject = st.text_input(
        "📚 Subject",
        placeholder="e.g. Artificial Intelligence"
    )

    topics_text = st.text_area(
        "📖 Topics / Chapters",
        placeholder=(
            "Enter topics separated by commas or one topic per line.\n\n"
            "Example:\n"
            "Machine Learning\n"
            "Neural Networks\n"
            "NLP\n"
            "Computer Vision"
        ),
        height=160
    )

    difficulty = st.selectbox(
        "🎯 Difficulty Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


with col2:
    exam_date = st.date_input(
        "📅 Exam Date",
        min_value=date.today(),
        value=date.today() + timedelta(days=7)
    )

    daily_hours = st.number_input(
        "⏰ Daily Study Hours",
        min_value=0.5,
        max_value=12.0,
        value=2.0,
        step=0.5
    )

    learning_style = st.selectbox(
        "📝 Preferred Study Style",
        [
            "Balanced",
            "Theory Focused",
            "Practice Focused",
            "Revision Focused"
        ]
    )


st.divider()


# ---------------------------------------------------------
# GENERATE PLAN
# ---------------------------------------------------------

generate_button = st.button(
    "🚀 Generate Smart Study Plan",
    type="primary",
    use_container_width=True
)


if generate_button:

    if not subject.strip():
        st.warning("Please enter a subject.")
        st.stop()

    if not topics_text.strip():
        st.warning("Please enter at least one topic.")
        st.stop()

    # Calculate available days
    days_available = (exam_date - date.today()).days + 1

    if days_available <= 0:
        st.error("Please select a future exam date.")
        st.stop()

    # Clean topics
    topics = []

    for line in topics_text.replace(",", "\n").splitlines():
        topic = line.strip()

        if topic and topic not in topics:
            topics.append(topic)

    st.session_state.study_topics = topics

    # Reset completed topics when a new plan is generated
    st.session_state.completed_topics = set()

    # -----------------------------------------------------
    # AI PROMPT
    # -----------------------------------------------------

    prompt = f"""
You are an expert AI Study Planner.

Create a professional and realistic study plan for a student.

Student Information:
Subject: {subject}
Topics:
{chr(10).join("- " + topic for topic in topics)}

Difficulty Level: {difficulty}
Exam Date: {exam_date.strftime("%d %B %Y")}
Days Available: {days_available}
Daily Study Time: {daily_hours} hours
Preferred Study Style: {learning_style}

Requirements:

1. Create a day-by-day study plan.
2. Distribute the topics realistically across the available days.
3. Do not overload one day.
4. Include revision before the exam.
5. Include practice questions or quizzes.
6. Include short breaks where appropriate.
7. Prioritize difficult topics.
8. Keep the plan practical for a student.
9. Use a professional markdown table.

The table should contain:

Day | Topics | Study Activity | Recommended Time

After the table, provide:

### Study Strategy
Give 3-5 short useful study tips.

### Final Revision
Explain what the student should revise before the exam.

Do not invent topics that are unrelated to the provided subject.
"""

    with st.spinner("🤖 AI is creating your personalized study plan..."):

        result = ask_ai(
            prompt,
            language="English"
        )

    st.session_state.study_plan = result
    st.session_state.planner_generated = True


# ---------------------------------------------------------
# DISPLAY GENERATED PLAN
# ---------------------------------------------------------

if st.session_state.planner_generated:

    st.divider()

    st.subheader("📅 Your Personalized Study Plan")

    st.markdown(st.session_state.study_plan)

    st.divider()

    # -----------------------------------------------------
    # TOPIC TRACKING
    # -----------------------------------------------------

    st.subheader("✅ Topic Completion")

    st.caption(
        "Mark topics as completed to update your Progress Dashboard."
    )

    for index, topic in enumerate(st.session_state.study_topics):

        completed = topic in st.session_state.completed_topics

        checkbox_value = st.checkbox(
            topic,
            value=completed,
            key=f"planner_topic_{index}"
        )

        if checkbox_value:
            st.session_state.completed_topics.add(topic)
        else:
            st.session_state.completed_topics.discard(topic)

    # -----------------------------------------------------
    # PROGRESS
    # -----------------------------------------------------

    total_topics = len(st.session_state.study_topics)
    completed_count = len(st.session_state.completed_topics)

    if total_topics > 0:

        progress = completed_count / total_topics

        st.progress(progress)

        st.write(
            f"**Progress:** {completed_count}/{total_topics} topics completed "
            f"({progress * 100:.0f}%)"
        )

    st.info(
        "💡 Your completed topics are automatically used by the "
        "Progress Dashboard during this session."
    )