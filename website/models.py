from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000))
    dateStart = db.Column(db.DateTime(timezone=True), default=func.now())
    dateEnd = db.Column(db.DateTime(timezone=True), default=func.now())
    priority = db.Column(db.String(100))
    mobility = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    events = db.relationship('Event')
