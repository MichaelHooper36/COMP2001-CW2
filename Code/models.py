# models.py

from datetime import datetime
import pytz

from marshmallow_sqlalchemy import fields

from config import db, ma

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'CW2'}
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(63), unique=True)
    email = db.Column(db.String(63), unique=True)
    password = db.Column(db.String(63))
    role = db.Column(db.String(5))


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True


user_schema = UserSchema()
people_schema = UserSchema(many=True)