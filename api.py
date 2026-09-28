from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import os
import json


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)


# --------------------------------------------------
# GEMINI CLIENT
# --------------------------------------------------

if not API_KEY:
    print(
        "WARNING: GEMINI_API_KEY is not configured."
    )
    client = None
else:
    client = genai.Client(
        api_key=API_KEY
    )


# --------------------------------------------------
# FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="EduGenie API",
    description="AI-powered learning assistant",
    version="1.0.0"
)


# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class QuestionRequest(BaseModel):
    question: str


class TopicRequest(BaseModel):
    topic: str


class SummaryRequest(BaseModel):
    text: str


class QuizRequest(BaseModel):
    topic: str
    number_of_questions: int = 5
    difficulty: str = "medium"


# --------------------------------------------------
# GEMINI FUNCTION
# --------------------------------------------------

def ask_gemini(prompt: str) -> str:

    if client is None:
        raise Exception(
            "Gemini API key is not configured."
        )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise Exception(
            "Gemini returned an empty response."
        )

    return response.text.strip()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "EduGenie API is running",
        "version": "1.0.0"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "gemini_configured": client is not None
    }


# --------------------------------------------------
# QUESTION AND ANSWER
# --------------------------------------------------

@app.post("/qa")
def question_answer(
    request: QuestionRequest
):

    try:

        prompt = f"""
You are EduGenie, an AI learning assistant.

Answer the student's question clearly
and accurately.

Student Question:
{request.question}

Instructions:

- Use simple language.
- Explain the answer clearly.
- Give an example when useful.
- Avoid unnecessary complicated words.
"""

        answer = ask_gemini(prompt)

        return {
            "success": True,
            "result": answer
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# EXPLANATION
# --------------------------------------------------

@app.post("/explain")
def explain(
    request: TopicRequest
):

    try:

        prompt = f"""
You are EduGenie, a college learning assistant.

Explain the following topic:

{request.topic}

Use this structure:

1. Definition
2. Simple explanation
3. Important points
4. Simple example
5. Real-world application

Use student-friendly language.
"""

        explanation = ask_gemini(prompt)

        return {
            "success": True,
            "result": explanation
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# SUMMARIZATION
# --------------------------------------------------

@app.post("/summarize")
def summarize(
    request: SummaryRequest
):

    try:

        prompt = f"""
You are EduGenie.

Summarize the following text.

Requirements:

- Keep the main ideas.
- Remove unnecessary information.
- Use simple language.
- Make the result shorter.
- Keep important facts.

Text:

{request.text}
"""

        summary = ask_gemini(prompt)

        return {
            "success": True,
            "result": summary
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# QUIZ GENERATION
# --------------------------------------------------

@app.post("/quiz")
def generate_quiz(
    request: QuizRequest
):

    try:

        prompt = f"""
You are EduGenie, an AI quiz generator.

Create a quiz about:

Topic:
{request.topic}

Number of questions:
{request.number_of_questions}

Difficulty:
{request.difficulty}

Create multiple-choice questions.

Each question must contain:

- question
- four options
- correct answer
- short explanation

Return ONLY valid JSON.

Use exactly this format:

{{
    "questions": [
        {{
            "question": "Question text",
            "options": [
                "Option A",
                "Option B",
                "Option C",
                "Option D"
            ],
            "answer": "Correct option",
            "explanation": "Short explanation"
        }}
    ]
}}
"""

        result = ask_gemini(prompt)

        # Remove markdown code fences if Gemini adds them
        result = result.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        ).strip()

        quiz = json.loads(result)

        return {
            "success": True,
            "result": quiz
        }

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail=(
                "Gemini returned an invalid "
                "quiz format."
            )
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# LEARNING RECOMMENDATIONS
# --------------------------------------------------

@app.post(
    "/learning-recommendations"
)
def learning_recommendations(
    request: TopicRequest
):

    try:

        prompt = f"""
You are EduGenie, an AI learning assistant.

Create a learning roadmap for:

{request.topic}

Include:

1. Beginner topics
2. Intermediate topics
3. Advanced topics
4. Practice activities
5. Mini project ideas
6. Revision tips
7. Recommended learning order

Keep the roadmap practical for a
college student.
"""

        recommendations = ask_gemini(
            prompt
        )

        return {
            "success": True,
            "result": recommendations
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )