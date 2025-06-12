from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.models.question import Question
from app.schemas.questions import QuestionCreate, QuestionSchema, QuestionUpdate
from app.schemas.common import MessageResponse
from app.models import db
import logging


# creating a log file to control errors
logger = logging.getLogger(__name__)

# creating a blueprint for questions table
questions_bp = Blueprint('questions', __name__, url_prefix='/questions')


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# to GET all questions
@questions_bp.route('/', methods=['GET'])
def get_questions():
    questions = Question.query.all()
    # creating a dictionary of all gotten questions like [{1: 'text', 2: 'text'}]
    serialized = [QuestionSchema(id=q.id, text=q.text, user_id=q.user.id, user_nickname=q.user.nickname).model_dump() for q in questions]

    # checking if any questions were found
    if questions:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No questions found").model_dump()), 404



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# to CREATE a new question
@questions_bp.route('/', methods=['POST'])
def create_question():
    logger.info('creating a question...')
    input_data = request.get_json() # getting a json "file" of question

    try:
        question_data = QuestionCreate(**input_data)
        question = Question(text=question_data.text, user_id=question_data.user_id)
        db.session.add(question)
        db.session.commit()
        return jsonify(MessageResponse(message="Your question was created!").model_dump()), 201
    except ValidationError as e:
        return jsonify({'error': e.errors}), 400



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# creating a function to GET question by ID with method "GET"
@questions_bp.route('/<int:id>', methods=['GET'])
def get_question(id):
    logger.info(f'getting question with {id}')
    question = Question.query.get(id)

    if question:
        return jsonify(MessageResponse(message=QuestionSchema(id=question.id,
                                                              text=question.text,
                                                              user_id=question.user.id,
                                                              user_nickname=question.user.nickname).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No question with id {id} was found.").model_dump())



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# creating a function to UPDATE a question by ID with method "PUT"
@questions_bp.route('/<int:id>', methods=['PUT'])
def update_question(id):
    question = Question.query.get(id)
    input_data = request.get_json()

    if question:
        try:
            updated_data = QuestionUpdate(**input_data)
            question.text, question.user_id = updated_data.text, updated_data.user_id
            db.session.commit()
            return jsonify(MessageResponse(message=f"The question with id {id} was updated.").model_dump()), 200
        except ValidationError as e:
            return jsonify({'error': e.errors}), 400
    else:
        return jsonify(MessageResponse(message=f"No question with id {id} was found.").model_dump()), 404



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# creating a function to DELETE a question
@questions_bp.route('/<int:id>', methods=['DELETE'])
def delete_question(id):
    question = Question.query.get(id)

    if question:
        db.session.delete(question)
        db.session.commit()
        return jsonify(MessageResponse(message=f"The question with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No question with id {id} was found.").model_dump()), 404
