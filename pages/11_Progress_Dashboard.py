import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Progress Dashboard",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "study_topics" not in st.session_state:
    st.session_state.study_topics = []

if "completed_topics" not in st.session_state:
    st.session_state.completed_topics = set()

if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = []

if "study_hours" not in st.session_state:
    st.session_state.study_hours = 0.0

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 Student Progress Dashboard")

st.write(
    "Track your learning progress, quiz performance, "
    "completed topics and study activity in one place."
)

st.divider()

# --------------------------------------------------
# CALCULATIONS
# --------------------------------------------------

total_topics = len(
    st.session_state.study_topics
)

completed_topics = len(
    st.session_state.completed_topics
)

if total_topics > 0:
    study_progress = (
        completed_topics / total_topics
    )
else:
    study_progress = 0

quiz_scores = st.session_state.quiz_scores

if quiz_scores:
    average_score = (
        sum(quiz_scores) / len(quiz_scores)
    )
else:
    average_score = 0

# --------------------------------------------------
# METRICS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Topics Completed",
        completed_topics
    )

with col2:
    st.metric(
        "📝 Quizzes",
        len(quiz_scores)
    )

with col3:
    st.metric(
        "🎯 Average Score",
        f"{average_score:.0f}%"
    )

with col4:
    st.metric(
        "📈 Study Progress",
        f"{study_progress * 100:.0f}%"
    )

st.divider()

# --------------------------------------------------
# STUDY PROGRESS
# --------------------------------------------------

st.subheader("📚 Learning Progress")

if total_topics == 0:

    st.info(
        "No study plan available yet. "
        "Create a plan from Smart Study Planner first."
    )

else:

    st.progress(study_progress)

    st.write(
        f"{completed_topics} of "
        f"{total_topics} topics completed."
    )

    remaining = (
        total_topics - completed_topics
    )

    if remaining == 0:

        st.success(
            "🎉 Excellent! All planned topics are completed."
        )

    else:

        st.warning(
            f"📖 {remaining} topic(s) remaining."
        )

st.divider()

# --------------------------------------------------
# TOPIC STATUS
# --------------------------------------------------

st.subheader("📋 Topic Status")

if total_topics == 0:

    st.write("No topics available.")

else:

    topic_data = []

    for topic in st.session_state.study_topics:

        if topic in st.session_state.completed_topics:
            status = "Completed"
        else:
            status = "Pending"

        topic_data.append(
            {
                "Topic": topic,
                "Status": status
            }
        )

    topic_df = pd.DataFrame(topic_data)

    st.dataframe(
        topic_df,
        use_container_width=True,
        hide_index=True
    )

st.divider()

# --------------------------------------------------
# QUIZ PERFORMANCE
# --------------------------------------------------

st.subheader("📝 Quiz Performance")

if not quiz_scores:

    st.info(
        "No quiz results recorded yet."
    )

else:

    quiz_data = []

    for index, score in enumerate(
        quiz_scores,
        start=1
    ):

        quiz_data.append(
            {
                "Quiz": f"Quiz {index}",
                "Score": score
            }
        )

    quiz_df = pd.DataFrame(
        quiz_data
    )

    st.dataframe(
        quiz_df,
        use_container_width=True,
        hide_index=True
    )

    st.line_chart(
        quiz_df.set_index("Quiz")["Score"]
    )

st.divider()

# --------------------------------------------------
# RECORD QUIZ RESULT
# --------------------------------------------------

st.subheader("➕ Record Quiz Result")

quiz_score = st.number_input(
    "Quiz Score (%)",
    min_value=0,
    max_value=100,
    value=0,
    step=1
)

if st.button(
    "💾 Save Quiz Result",
    use_container_width=True
):

    st.session_state.quiz_scores.append(
        float(quiz_score)
    )

    st.success(
        f"✅ Quiz result saved: {quiz_score}%"
    )

    st.rerun()

st.divider()

# --------------------------------------------------
# STUDY TIME
# --------------------------------------------------

st.subheader("⏰ Study Time Tracker")

study_hours = st.number_input(
    "Add Study Hours",
    min_value=0.0,
    max_value=24.0,
    value=0.0,
    step=0.5
)

if st.button(
    "➕ Add Study Time",
    use_container_width=True
):

    st.session_state.study_hours += study_hours

    st.success(
        f"✅ {study_hours:.1f} study hours added."
    )

    st.rerun()

st.metric(
    "Total Study Hours",
    f"{st.session_state.study_hours:.1f} hrs"
)

st.divider()

# --------------------------------------------------
# AREAS TO IMPROVE
# --------------------------------------------------

st.subheader("🎯 Areas to Improve")

pending_topics = [
    topic
    for topic in st.session_state.study_topics
    if topic not in st.session_state.completed_topics
]

if pending_topics:

    for topic in pending_topics:

        st.write(
            f"🔸 {topic}"
        )

else:

    if total_topics > 0:

        st.success(
            "🌟 No pending topics. "
            "Keep revising to stay prepared!"
        )

    else:

        st.info(
            "Create a study plan to identify "
            "areas for improvement."
        )

st.divider()

# --------------------------------------------------
# PERFORMANCE INSIGHT
# --------------------------------------------------

st.subheader("💡 Performance Insight")

if average_score >= 80:

    st.success(
        "🌟 Excellent performance! "
        "Keep practicing and focus on revision."
    )

elif average_score >= 60:

    st.info(
        "👍 Good progress! "
        "Review weak areas and continue practicing."
    )

elif average_score > 0:

    st.warning(
        "📖 More practice is recommended. "
        "Review the topics where you struggled."
    )

else:

    st.info(
        "Complete a quiz to receive "
        "personalized performance feedback."
    )