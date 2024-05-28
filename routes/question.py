# routes/question.py

from fastapi import APIRouter, HTTPException
from typing import List
from schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from services.question import create_question, get_question, get_questions, update_question, delete_question

question_router = APIRouter(
    prefix="/questions",
    tags=["Question"],
    responses={404: {"description": "Not found"}},
)

@question_router.post("/", response_model=QuestionResponse, summary="Create a new question", description="Create a new question and return the question details.")
def create_new_question(question_data: QuestionCreate):
    question = create_question(question_data)
    return question

@question_router.get("/{question_id}", response_model=QuestionResponse, summary="Get question details", description="Retrieve details of a question by its ID.")
def read_question(question_id: str):
    question = get_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@question_router.get("/", response_model=List[QuestionResponse], summary="Get list of questions", description="Retrieve a list of questions with pagination.")
def read_questions():
    questions = get_questions()
    return questions

@question_router.put("/{question_id}", response_model=QuestionResponse, summary="Update question details", description="Update details of a question by its ID.")
def update_question_data(question_id: str, question_data: QuestionUpdate):
    question = update_question(question_id, question_data)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@question_router.delete("/{question_id}", response_model=QuestionResponse, summary="Delete a question", description="Delete a question by its ID and return the deleted question details.")
def delete_question_data(question_id: str):
    question = delete_question(question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
