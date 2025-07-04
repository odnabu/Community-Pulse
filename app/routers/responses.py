# app/routers/responses.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.response import Response
from app.models.question import Question, Statistic
from app.schemas.common import MessageResponse, StatisticSchema
from app.schemas.responses import ResponseCreate, ResponseSchema, ResponseUpdate
from app.models import db
import logging


# creating a log file to control errors
logger = logging.getLogger(__name__)


responses_bp = Blueprint('responses', __name__, url_prefix='/responses')


# ===============================================================================================================
# creating a function to GET ALL responses with method "GET"
@responses_bp.route('/', methods=['GET'])
def get_responses():
    responses = Response.query.all()
    serialized = [ResponseSchema(question_text=r.question.text,
                                 is_agree=r.is_agree,
                                 question_id=r.question.id,
                                 id=r.id,
                                 text=r.text,
                                 user_id=r.user.id,
                                 user_nickname=r.user.nickname).model_dump() for r in responses]

    if responses:
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No responses found").model_dump()), 404


# ===============================================================================================================
# # creating a function to CREATE a response with method "POST"
# @responses_bp.route('/', methods=['POST'])
# def create_response():
#     input_data = request.get_json()
#     try:
#         response_data = ResponseCreate(**input_data)
#         response = Response(question_id=response_data.question_id,
#                             is_agree=response_data.is_agree,
#                             text=response_data.text,
#                             user_id=response_data.user_id)
#         db.session.add(response)
#         db.session.commit()
#         return jsonify(MessageResponse(message="Your response was created!").model_dump()), 200
#     except ValidationError as e:
#         return jsonify({'error': e.errors}), 400

# ОБНОВЛЕННАЯ функция для СОЗДАНИЯ (CREATE) ответа на вопрос методом "POST" и сразу же
# ЗАПИСЬЮ статистики в таблицу STATISTICS:
@responses_bp.route('/', methods=['POST'])
def create_response():
    input_data = request.get_json()
    try:
        response_data = ResponseCreate(**input_data)

        # Создание нового ответа  --->  ТУТ можно было бы доработать размещение только ОДНОГО ответа
        # от одного пользователя (см. закомментированный код).
        response = Response(
            question_id=response_data.question_id,
            is_agree=response_data.is_agree,
            text=response_data.text,
            user_id=response_data.user_id
        )
        # if not response.is_agree:
        #     db.session.add(response)
        # else:
        #     return f"You have sent a response on this question: {response.text} yet."
        db.session.add(response)

        # Обновление статистики
        stat = Statistic.query.get(response_data.question_id)
        if not stat:
            # Если записи ещё нет — создаём новую
            stat = Statistic(
                question_id=response_data.question_id,
                agree_count=1 if response_data.is_agree else 0,
                disagree_count=0 if response_data.is_agree else 1
            )
            db.session.add(stat)
        else:
            # Если запись есть — обновляем
            if response_data.is_agree:
                stat.agree_count += 1
            else:
                stat.disagree_count += 1

        db.session.commit()
        return jsonify(MessageResponse(message="Your response was created and statistics updated!").model_dump()), 200

    except ValidationError as e:
        return jsonify({'error': e.errors()}), 400



# ===============================================================================================================
# creating a function to GET response by ID with method "GET"
@responses_bp.route('/<int:id>', methods=['GET'])
def get_response(id):
    response = Response.query.get(id)

    if response:
        return jsonify(MessageResponse(message=ResponseSchema(question_text=response.question.text,
                                                              is_agree=response.is_agree,
                                                              question_id=response.question.id,
                                                              id=response.id,
                                                              text=response.text,
                                                              user_id=response.user.id,
                                                              user_nickname=response.user.nickname).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump())


# ===============================================================================================================
# creating a function to UPDATE a response by ID with method "PUT"
@responses_bp.route('/<int:id>', methods=['PUT'])
def update_response(id):
    response = Response.query.get(id)
    input_data = request.get_json()

    if response:
        try:
            updated_data = ResponseUpdate(**input_data)
            response.is_agree = updated_data.is_agree
            response.user_id = updated_data.user_id
            response.question_id = updated_data.question_id
            db.session.commit()
            return jsonify(MessageResponse(message=f"The response with id {id} was updated.").model_dump()), 200
        except ValidationError as e:
            return jsonify({'error': e.errors}), 400
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404


# ===============================================================================================================
# creating a function to DELETE an answer to the question by ID with method "DELETE"
@responses_bp.route('/<int:id>', methods=['DELETE'])
def delete_response(id):
    response = Response.query.get(id)

    if response:
        db.session.delete(response)
        db.session.commit()
        return jsonify(MessageResponse(message=f"The response with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No response with id {id} was found.").model_dump()), 404




""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%____      STATISTICS     ____%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """

# Статистика - сколько ответов получено ВСЕГО:
@responses_bp.route('/statistics/', methods=['GET'])
def get_statistics_responses():
    total_responses = db.session.query(Response).count()

    return {
        "total_responses": total_responses,
    }

# ===============================================================================================================
# Сколько всего положительных ответов (is_agree=True):
@responses_bp.route('/statistics/agree', methods=['GET'])
def get_agree_count():
    agree_count = db.session.query(Response).filter_by(is_agree=True).count()
    return jsonify(MessageResponse(message={"agree_count": agree_count}).model_dump()), 200

# ===============================================================================================================
# Сколько всего отрицательных ответов (is_agree=False)
@responses_bp.route('/statistics/disagree', methods=['GET'])
def get_disagree_count():
    disagree_count = db.session.query(Response).filter_by(is_agree=False).count()
    return jsonify(MessageResponse(message={"disagree_count": disagree_count}).model_dump()), 200

# ===============================================================================================================
# Сколько ответов получено на вопрос с определённым question_id:
@responses_bp.route('/statistics/question/<int:question_id>', methods=['GET'])
def get_response_count_for_question(question_id):
    count = db.session.query(Response).filter_by(question_id=question_id).count()
    return jsonify(MessageResponse(message={"question_id": question_id, "response_count": count}).model_dump()), 200


# ===============================================================================================================
# Красивый вывод КАРТОЧЕК со статистикой на странице браузера:
from flask import render_template
from app.models.question import Question

@responses_bp.route('/statistics/view', methods=['GET'])
def show_statistics_html():
    questions = Question.query.all()
    stats = []

    for q in questions:
        agree = sum(1 for r in q.responses if r.is_agree)
        disagree = sum(1 for r in q.responses if not r.is_agree)
        stats.append({
            "question": q.text,
            "agree": agree,
            "disagree": disagree
        })

    return render_template("statistics_view.html", stats=stats)


# ===============================================================================================================
# Расширенный API /statistics/, который:
#   1. Отображает статистику по всем вопросам.
#   2. Показывает:
#       - текст вопроса,
#       - количество согласных (agree_count),
#       - количество несогласных (disagree_count),
#       - общее количество ответов.
@responses_bp.route('/statistics/full/', methods=['GET'])
def get_full_statistics():
    statistics = db.session.query(Statistic).all()
    result = []

    for stat in statistics:
        question = Question.query.get(stat.question_id)
        if question:
            result.append(
                StatisticSchema(
                    question_text=question.text,
                    agree_count=stat.agree_count,
                    disagree_count=stat.disagree_count
                ).model_dump()
            )

    if result:
        return jsonify(MessageResponse(message=result).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No statistics found").model_dump()), 404



# ===============================================================================================================
# HTML-шаблон для вывода статистики в браузере:
@responses_bp.route('/statistics-html', methods=['GET'])
def statistics_html():
    statistics = db.session.query(Statistic).all()
    result = []

    for stat in statistics:
        question = Question.query.get(stat.question_id)
        if question:
            result.append({
                "question_text": question.text,
                "agree_count": stat.agree_count,
                "disagree_count": stat.disagree_count
            })

    return render_template('statistics_full.html', statistics=result)



