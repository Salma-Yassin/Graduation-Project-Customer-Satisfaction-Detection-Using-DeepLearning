
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    #name = db.Column(db.String(150), nullable=False)
    #locations = relationship(
    #    "UserLocations", backref="Users", passive_deletes=True)
    #members = relationship(
    #    "UserMembers", backref="Users", passive_deletes=True)
    # media = relationship("Media", backref="Users", passive_deletes=True)


    # created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    # User Data
class UserLocations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'),
                        nullable=False)


class UserMembers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'),
                        nullable=False)
    location_id = db.Column(db.ForeignKey(UserLocations.id), nullable=False)


class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(150), unique=True, nullable=False)
    #location_id = db.Column(db.ForeignKey(UserLocations.id))
    location_address = db.Column(db.String(150), nullable=False)
    #member_id = db.Column(db.ForeignKey(UserMembers.id))
    member_id = db.Column(db.Integer)
    type = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.ForeignKey(User.id, ondelete='CASCADE'),nullable=False)

    results = relationship(
        "AnalysisResults", backref="Media", passive_deletes=True)


class AnalysisResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.ForeignKey(Media.id, ondelete='CASCADE'),
                         nullable=False)
    result = db.Column(db.String)
    # Other Analysis Data