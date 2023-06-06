
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from dataclasses import dataclass
import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    companyName = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.Integer, nullable = False)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'role'
    }

class AdminUser(User):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    

class RegularUser(User):

    __tablename__ = 'regular'
    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity': 'regular'
    }

   
    
@dataclass
class UserLocations(db.Model):
    id : int
    name : str
    companyName : str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    companyName = db.Column(db.ForeignKey(User.companyName, ondelete='CASCADE'),nullable=False)


@dataclass
class UserMembers(db.Model):
    id : int
    name : str
    companyName : str
    member_id : int
    gender : str
    location_id : int  

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    companyName = db.Column(db.ForeignKey(User.companyName, ondelete='CASCADE'),nullable=False)
    member_id = db.Column(db.Integer, nullable=False, unique=True)
    gender = db.Column(db.String, nullable=False)
    location_id = db.Column(db.ForeignKey(UserLocations.id), nullable=False)



@dataclass
class Media(db.Model):
    id : int 
    media_name : str
    url : str
    location_address : str
    member_id : int
    type : str
    companyName : str
    results : str
    detailed_results : str
    created_at : datetime.datetime
    
    id = db.Column(db.Integer, primary_key=True)
    media_name = db.Column(db.String(150),unique= True, nullable=False)
    url = db.Column(db.String(150), nullable=False)
    #location_id = db.Column(db.ForeignKey(UserLocations.id))
    location_address = db.Column(db.String(150), nullable=False)
    #member_id = db.Column(db.ForeignKey(UserMembers.id))
    member_id = db.Column(db.Integer)
    type = db.Column(db.String(), nullable=False)
    companyName = db.Column(db.ForeignKey(User.companyName, ondelete='CASCADE'),nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    results = db.Column(db.String(150), nullable=False)
    detailed_results = db.Column(db.String(150), nullable=False)
    #results = relationship("AnalysisResults", backref="Media", passive_deletes=True)

@dataclass
class AnalysisResults(db.Model):
    id : int
    media_id : int
    results : str
    
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.ForeignKey(Media.id, ondelete='CASCADE'),
                         nullable=False)
    results = db.Column(db.String)
    # Other Analysis Data
    
    
    
####ADDED NEWLY FOR FEEDBACK

@dataclass
class Feedback(db.Model):
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    email = db.Column(db.String(150),unique=True, nullable=False)
    message = db.Column(db.Text)
    

@dataclass
class Contact(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    message = db.Column(db.Text)    

