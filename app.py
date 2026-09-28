import streamlit as st
import requests


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="EduGenie",
    page_icon="🎓",
    layout="centered"
)


# --------------------------------------------------
# BACKEND URL
# --------------------------------------------------

BACKEND_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .section {
        font-size: 25px;
        font-weight: bold;
        margin-top: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">'
    '🎓 EduGenie'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI-Powered Learning Assistant'
    '</div>',
    unsafe_allow_html=True
)


st.divider()


# --------------------------------------------------
# BACKEND CONNECTION FUNCTION
# --------------------------------------------------

def call_backend(
    endpoint,
    data
):

    try:

        response = requests.post(
            BACKEND_URL + endpoint,
            json=data,
            timeout=120
        )

        if response.status_code == 200:

            return response.json()

        else:

            try:
                error = response.json()
            except:
                error = response.text

            st.error(
                f"Backend Error: {error}"
            )

            return None

    except requests.exceptions.ConnectionError:

        st.error(
            "Cannot connect to EduGenie backend.\n\n"
            "Please make sure api.py is running."
        )

        return None

    except requests.exceptions.Timeout:

        st.error(
            "The request took too long. "
            "Please try again."
        )

        return None

    except Exception as error:

        st.error(
            f"Error: {error}"
        )

        return None


# ==================================================
# 1. ASK A QUESTION
# ==================================================

st.markdown(
    '<div class="section">'
    '💬 Ask EduGenie a Question'
    '</div>',
    unsafe_allow_html=True
)

question = st.text_area(
    "Enter your question:",
    placeholder=(
        "Example: What is artificial intelligence?"
    ),
    height=120
)


if st.button(
    "🤖 Get Answer",
    use_container_width=True
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "EduGenie is thinking..."
        ):

            data = call_backend(
                "/qa",
                {
                    "question":
                        question
                }
            )

        if data:

            st.success("Answer")

            st.write(
                data["result"]
            )


st.divider()


# ==================================================
# 2. EXPLAIN A TOPIC
# ==================================================

st.markdown(
    '<div class="section">'
    '📚 Need an Explanation?'
    '</div>',
    unsafe_allow_html=True
)

topic = st.text_input(
    "Enter a topic:",
    placeholder=(
        "Example: Machine Learning"
    )
)


if st.button(
    "📖 Explain Topic",
    use_container_width=True
):

    if not topic.strip():

        st.warning(
            "Please enter a topic."
        )

    else:

        with st.spinner(
            "Preparing explanation..."
        ):

            data = call_backend(
                "/explain",
                {
                    "topic":
                        topic
                }
            )

        if data:

            st.success("Explanation")

            st.write(
                data["result"]
            )


st.divider()


# ==================================================
# 3. SUMMARIZE
# ==================================================

st.markdown(
    '<div class="section">'
    '📝 Summarize a Paragraph'
    '</div>',
    unsafe_allow_html=True
)

text = st.text_area(
    "Paste your text:",
    placeholder=(
        "Paste the paragraph or notes "
        "you want to summarize here..."
    ),
    height=180
)


if st.button(
    "✨ Summarize",
    use_container_width=True
):

    if not text.strip():

        st.warning(
            "Please enter some text."
        )

    else:

        with st.spinner(
            "Creating summary..."
        ):

            data = call_backend(
                "/summarize",
                {
                    "text":
                        text
                }
            )

        if data:

            st.success("Summary")

            st.write(
                data["result"]
            )


st.divider()


# ==================================================
# 4. QUIZ GENERATOR
# ==================================================

st.markdown(
    '<div class="section">'
    '🧠 Generate a Quiz'
    '</div>',
    unsafe_allow_html=True
)

quiz_topic = st.text_input(
    "Quiz topic:",
    placeholder="Example: Python Programming"
)


col1, col2 = st.columns(2)


with col1:

    number_of_questions = st.number_input(
        "Number of questions",
        min_value=1,
        max_value=10,
        value=5,
        step=1
    )


with col2:

    difficulty = st.selectbox(
        "Difficulty",
        [
            "easy",
            "medium",
            "hard"
        ]
    )


if st.button(
    "🎯 Generate Quiz",
    use_container_width=True
):

    if not quiz_topic.strip():

        st.warning(
            "Please enter a quiz topic."
        )

    else:

        with st.spinner(
            "Generating quiz..."
        ):

            data = call_backend(
                "/quiz",
                {
                    "topic":
                        quiz_topic,

                    "number_of_questions":
                        number_of_questions,

                    "difficulty":
                        difficulty
                }
            )

        if data:

            quiz = data["result"]

            st.session_state[
                "quiz"
            ] = quiz


# --------------------------------------------------
# DISPLAY QUIZ
# --------------------------------------------------

if "quiz" in st.session_state:

    quiz = st.session_state[
        "quiz"
    ]

    st.subheader(
        "📋 Your Quiz"
    )

    user_answers = {}

    for index, question in enumerate(
        quiz["questions"]
    ):

        st.write(
            f"### Question {index + 1}"
        )

        st.write(
            question["question"]
        )

        user_answers[index] = st.radio(
            "Choose your answer:",
            question["options"],
            key=f"answer_{index}"
        )

    if st.button(
        "✅ Check My Answers",
        use_container_width=True
    ):

        score = 0

        for index, question in enumerate(
            quiz["questions"]
        ):

            if (
                user_answers[index]
                == question["answer"]
            ):

                score += 1

        total = len(
            quiz["questions"]
        )

        st.success(
            f"Your Score: {score}/{total}"
        )

        st.subheader(
            "Answer Review"
        )

        for index, question in enumerate(
            quiz["questions"]
        ):

            st.write(
                f"**Question {index + 1}:** "
                f"{question['answer']}"
            )

            st.caption(
                question["explanation"]
            )


st.divider()


# ==================================================
# 5. LEARNING RECOMMENDATIONS
# ==================================================

st.markdown(
    '<div class="section">'
    '🚀 Learning Recommendations'
    '</div>',
    unsafe_allow_html=True
)

learning_topic = st.text_input(
    "What do you want to learn?",
    placeholder=(
        "Example: Data Science"
    )
)


if st.button(
    "🗺️ Create Learning Path",
    use_container_width=True
):

    if not learning_topic.strip():

        st.warning(
            "Please enter a topic."
        )

    else:

        with st.spinner(
            "Creating your learning path..."
        ):

            data = call_backend(
                "/learning-recommendations",
                {
                    "topic":
                        learning_topic
                }
            )

        if data:

            st.success(
                "Your Learning Path"
            )

            st.write(
                data["result"]
            )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "EduGenie - Google Gemini Powered "
    "Learning Assistant"
)

st.caption(
    "Built with Streamlit + FastAPI + Gemini AI"
)