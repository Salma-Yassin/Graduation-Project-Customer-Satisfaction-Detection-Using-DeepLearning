from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    # created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    # User Data


class UserLocations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.ForeignKey(Users.id), nullable=False)


class UserMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.ForeignKey(Users.id), nullable=False)
    location_id = db.Column(db.ForeignKey(UserLocations.id), nullable=False)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(150), unique=True, nullable=False)
    location_id = db.Column(db.ForeignKey(UserLocations.id))
    member_id = db.Column(db.ForeignKey(UserMembers.id))
    type = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.ForeignKey(Users.id), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())


class AnalysisResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.ForeignKey(Media.id), nullable=False)
    result = db.Column(db.String)
    # Other Analysis Data
