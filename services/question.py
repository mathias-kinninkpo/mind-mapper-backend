# services/question.py

from typing import List, Optional
from models.question import Question as QuestionModel
from schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse
from bson import ObjectId

def create_question(question_data: QuestionCreate) -> QuestionResponse:
    question = QuestionModel(content=question_data.content, identifiant=question_data.identifiant)
    question.save()
    question_dict = question.to_mongo().to_dict()
    question_dict['id'] = str(question_dict['_id'])
    question_response = QuestionResponse.parse_obj(question_dict)
    return question_response

def get_question(question_id: str) -> Optional[QuestionResponse]:
    question = QuestionModel.objects(id=ObjectId(question_id)).first()
    if question:
        question_dict = question.to_mongo().to_dict()
        question_dict['id'] = str(question_dict['_id'])
        question_response = QuestionResponse.parse_obj(question_dict)
        return question_response
    return None

def get_questions() -> List[QuestionResponse]:
    questions = QuestionModel.objects.all()
    question_responses = []
    for question in questions:
        question_dict = question.to_mongo().to_dict()
        question_dict['id'] = str(question_dict['_id'])
        question_responses.append(QuestionResponse.parse_obj(question_dict))
    return question_responses

def update_question(question_id: str, question_data: QuestionUpdate) -> Optional[QuestionResponse]:
    question = QuestionModel.objects(id=ObjectId(question_id)).first()
    if question:
        question.update(content=question_data.content)
        question.reload()
        question_dict = question.to_mongo().to_dict()
        question_dict['id'] = str(question_dict['_id'])
        question_response = QuestionResponse.parse_obj(question_dict)
        return question_response
    return None

def delete_question(question_id: str) -> Optional[QuestionResponse]:
    question = QuestionModel.objects(id=ObjectId(question_id)).first()
    question_dict = question.to_mongo().to_dict()
    question_dict['id'] = str(question_dict['_id'])
    if question:
        question_response = QuestionResponse.parse_obj({
            'id': question_dict['id'],
            'content': question.content,
            'identifiant': question.identifiant
        })
        question.delete()
        return question_response
    return None
