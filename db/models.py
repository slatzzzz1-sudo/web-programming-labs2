from . import db
from flask_login import UserMixin
from datetime import datetime


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(162), nullable=False)


class articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(50), nullable=False)
    article_text = db.Column(db.Text, nullable=False)
    is_favorite = db.Column(db.Boolean)
    is_public = db.Column(db.Boolean)
    likes = db.Column(db.Integer)

class postcards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wish = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.String(100), default="Гость")
    created_at = db.Column(db.DateTime, default=datetime.now)
    likes = db.Column(db.Integer, default=0)
    card_type = db.Column(db.Integer, default=0)  # 0-7 для типов открыток    


class GiftBox(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_opened = db.Column(db.Boolean, default=False)
    position_x = db.Column(db.Integer)
    position_y = db.Column(db.Integer)    

