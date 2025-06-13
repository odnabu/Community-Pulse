# app/routers/users.py

from flask import Blueprint, jsonify, request
from pydantic import ValidationError
from app.models.user import User
from app.schemas.common import MessageResponse
from app.schemas.users import UserCreate, UserSchema, UserDelete, UserUpdate
from app.models import db
import logging


# creating a log file to control errors
logger = logging.getLogger(__name__)

# creating a blueprint for table "users"
users_bp = Blueprint('users', __name__, url_prefix='/users')


# ===============================================================================================================
# to GET all users
@users_bp.route('/', methods=['GET'])
def get_users():
    founded_users = User.query.all()

    if founded_users:
        serialized = [UserSchema(id=u.id, nickname=u.nickname).model_dump() for u in founded_users]
        return jsonify(MessageResponse(message=serialized).model_dump()), 200
    else:
        return jsonify(MessageResponse(message='No user was found.').model_dump()), 404


# ===============================================================================================================
# to CREATE a new user
@users_bp.route('/', methods=['POST'])
def create_user():
    input_data = request.get_json()

    try:
        userdata = UserCreate(**input_data)
        user = User(nickname=userdata.nickname, password=userdata.password)
        db.session.add(user)
        db.session.commit()
        logger.info(f'| new user {user.nickname} was created |')
        return jsonify(MessageResponse(message='User was created').model_dump()), 201
    except ValidationError as e:
        logger.error('| unknown error |')
        return jsonify(MessageResponse(message='Unknown error. Try again.').model_dump()), 400


# ===============================================================================================================
# to GET one user by ID
@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)

    if user:
        return jsonify(MessageResponse(message=UserSchema(  id=user.id,
                                                            nickname=user.nickname).model_dump()).model_dump())
    else:
        return jsonify(MessageResponse(message=f"No user with id {id} was found.").model_dump())


# ===============================================================================================================
# to UPDATE / CHANGE an existed user
@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    input_data = request.get_json()

    if user:
        try:
            updated_data = UserUpdate(**input_data)
            user.nickname = updated_data.nickname
            user.password = updated_data.password
            db.session.commit()
            return jsonify(MessageResponse(message=f"The user with id {id} was updated.").model_dump()), 200
        except ValidationError as e:
            return jsonify({'error': e.errors}), 400
    else:
        return jsonify(MessageResponse(message=f"No user with id {id} was found.").model_dump()), 404


# ===============================================================================================================
# creating a function to DELETE a user
@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify(MessageResponse(message=f"The user with id {id} was deleted.").model_dump()), 200
    else:
        return jsonify(MessageResponse(message=f"No user with id {id} was found.").model_dump()), 404


""" %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%____      STATISTICS     ____%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% """

# Сколько всего пользователей зарегистрировано
@users_bp.route('/statistics/count', methods=['GET'])
def get_user_count():
    from app.models.user import User
    count = db.session.query(User).count()
    return jsonify(MessageResponse(message={"user_count": count}).model_dump()), 200

