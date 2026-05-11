from datetime import datetime
from flask_login import UserMixin
from db import db


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    tasks = db.relationship('Task', backref='user', lazy=True)


class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    priority = db.Column(db.String(50))

    status = db.Column(db.String(50), default='Pending')

    created_date = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))