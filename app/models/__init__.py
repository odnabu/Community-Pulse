# app/models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.models.question import *
from app.models.response import *
from app.models.user import *
from app.models.category import *
