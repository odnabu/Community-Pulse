# app/routers/categories.py

from flask import Blueprint, jsonify, request, abort
from pydantic import ValidationError
from app.schemas.common import MessageResponse
from app.schemas.categories import CategoryCreate, CategorySchema
from app.models import db, Category, Question, Response
from sqlalchemy import func
import logging


# creating a log file to control errors
logger = logging.getLogger(__name__)


categories_bp = Blueprint('categories', __name__, url_prefix='/categories')



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# to GET all categories
@categories_bp.route('/', methods=['GET'])
def get_categories():
    all_categories = Category.query.all()

    if all_categories:
        serialized = [CategorySchema(id=ac.id, name=ac.name).model_dump() for ac in all_categories]
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message="No categories found").model_dump()), 404


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# to CREATE a new category
@categories_bp.route('/', methods=['POST'])
def create_category():
    input_data = request.get_json()

    try:
        category_name = CategoryCreate(**input_data)
        category = Category(name=category_name.name)
        db.session.add(category)
        db.session.commit()
        # logger.info(f"| new category \"{category.name}\" was created |")
        return jsonify(MessageResponse(message='Category was created!').model_dump()), 201
    except ValidationError as e:
        # logger.error('| unknown error |')
        # return jsonify(MessageResponse(message='Unknown error. Try again.').model_dump()), 400
        return jsonify({'error': e.errors}), 400



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# to GET one category by ID
@categories_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)

    if category:
        return jsonify(MessageResponse(message=CategorySchema(  id=category.id,
                                                                name=category.name).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No category with id {id} was found.").model_dump())





# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Статистика:
@categories_bp.route("/categories/<int:category_id>", methods=["GET"])
def get_category_stats(category_id):
    category = Category.query.get(category_id)
    if not category:
        abort(404, description="Category not found")

    questions_data = []

    for question in category.questions:
        total = db.session.query(func.count(Response.id))\
            .filter(Response.question_id == question.id).scalar()

        agree = db.session.query(func.count(Response.id)) \
            .filter(Response.question_id == question.id, Response.is_agree == True).scalar()

        disagree = db.session.query(func.count(Response.id)) \
            .filter(Response.question_id == question.id, Response.is_agree == False).scalar()

        questions_data.append({
            "question_id": question.id,
            "question_text": question.text,
            "total_responses": total,
            "agree": agree,
            "disagree": disagree
        })

    return jsonify({
        "category_id": category.id,
        "category_name": category.name,
        "questions": questions_data
    })

