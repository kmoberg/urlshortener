from flask_login import UserMixin
from sqlalchemy import func

from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


class Urls(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, nullable=False, default=func.now())
    original_url = db.Column(db.Text, nullable=False)
    generated_user = db.Column(db.Integer, nullable=False)
    clicks = db.Column(db.Integer, nullable=False, default=0)
