import streamlit as st
from datetime import date, timedelta
from utils.ai_engine import ask_ai

st.set_page_config(
    page_title="Smart Study Planner",
    page_icon="🧠",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "study_topics" not in st.session_state:
    st.session_state.study_topics = []

if "completed_topics" not in st.session_state:
    st.session_state.completed_topics = set()

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🧠 Smart Study Planner")

st.write(
    "Create a personalized AI-powered study plan based on your "
    "subject, topics, exam date, study hours and learning style."
)

st.divider()

# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    subject = st.text_input(
        "📚 Subject",
        placeholder="e.g. Artificial Intelligence"
    )

    topics = st.text_area(
        "📖 Topics / Chapters",
        placeholder="Enter topics separated by commas",
        height=150
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
        value=date.today() + timedelta(days=7),
        min_value=date.today()
    )

    daily_hours = st.number_input(
        "⏰ Daily Study Hours",
        min_value=0.5,
        max_value=12.0,
        value=2.0,
        step=0.5
    )

    study_style = st.selectbox(
        "📝 Study Style",
        [
            "Balanced",
            "Theory Focused",
            "Practice Focused",
            "Revision Focused"
        ]
    )

st.divider()

# --------------------------------------------------
# GENERATE PLAN
# --------------------------------------------------

if st.button(
    "🚀 Generate Smart Study Plan",
    type="primary",
    use_container_width=True
):

    if not subject.strip():
        st.warning("Please enter a subject.")
        st.stop()

    if not topics.strip():
        st.warning("Please enter your topics.")
        st.stop()

    # Convert topics into a clean list
    topic_list = [
        topic.strip()
        for topic in topics.split(",")
        if topic.strip()
    ]

    # Save topics for Progress Dashboard
    st.session_state.study_topics = topic_list

    # Reset completed topics for new plan
    st.session_state.completed_topics = set()

    days = (exam_date - date.today()).days + 1

    # --------------------------------------------------
    # AI PROMPT
    # --------------------------------------------------

    prompt = f"""
You are an expert AI Study Planner.

Create a personalized and realistic study plan.

Subject:
{subject}

Topics:
{", ".join(topic_list)}

Difficulty:
{difficulty}

Exam Date:
{exam_date.strftime("%d %B %Y")}

Days Available:
{days}

Daily Study Time:
{daily_hours} hours

Study Style:
{study_style}

Create a day-by-day study plan.

Use exactly this format:

| Day | Topics | Activity | Time |

Include:
- Learning
- Practice
- Revision
- Quiz or practice questions
- Final revision before the exam

After the table provide:

### Study Strategy

Give 3-5 short and practical study tips.

Keep the plan simple, realistic and student-friendly.
"""

    # --------------------------------------------------
    # AI RESPONSE
    # --------------------------------------------------

    with st.spinner(
        "🤖 Creating your personalized study plan..."
    ):

        result = ask_ai(
            prompt,
            language="English"
        )

    st.divider()

    st.subheader("📅 Your Personalized Study Plan")

    st.markdown(result)

    st.success(
        "✅ Study plan generated successfully!"
    )

# --------------------------------------------------
# TOPIC TRACKER
# --------------------------------------------------

if st.session_state.study_topics:

    st.divider()

    st.subheader("✅ Topic Completion Tracker")

    st.write(
        "Mark the topics you have completed. "
        "Your progress will appear in the Progress Dashboard."
    )

    for topic in st.session_state.study_topics:

        checked = st.checkbox(
            topic,
            value=topic in st.session_state.completed_topics,
            key=f"topic_{topic}"
        )

        if checked:
            st.session_state.completed_topics.add(topic)
        else:
            st.session_state.completed_topics.discard(topic)

    total = len(st.session_state.study_topics)
    completed = len(st.session_state.completed_topics)

    if total > 0:
        progress = completed / total

        st.progress(progress)

        st.write(
            f"📊 Progress: {completed}/{total} topics completed "
            f"({progress * 100:.0f}%)"
        )