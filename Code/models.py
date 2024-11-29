# models.py

from datetime import datetime
import pytz

from marshmallow_sqlalchemy import fields

from config import db, ma

class User(db.Model):
    __tablename__ = "person"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    timestamp = db.Column(
        db.DateTime, default=lambda: datetime.now(pytz.timezone('Europe/London')),
    onupdate=lambda: datetime.now(pytz.timezone('Europe/London'))
    )
    notes = db.relationship(
        "Note",
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True


user_schema = UserSchema()
people_schema = UserSchema(many=True)