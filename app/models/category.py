# app/models/category.py

from app.models import db

class Category(db.Model):
    __tablename__ = 'categories'

    # Столбцы (поля):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    # Связь с моделью Question:
    questions = db.relationship('Question', back_populates='category', lazy=True)

    def __repr__(self):
        return f'ID: {self.id}\nCategory: {self.name}'
