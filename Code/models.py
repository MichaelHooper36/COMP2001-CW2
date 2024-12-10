# models.py

from marshmallow_sqlalchemy import fields
from marshmallow import validates, ValidationError

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

class Location(db.Model):
    __tablename__ = "location_point"
    __table_args__ = {'schema': 'CW2'}
    location_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    description = db.Column(db.String(500))

    @validates('longitude')
    def validate_longitude(self, value):
        if not -180 <= value <= 180:
            raise ValidationError('Longitude must be between -180 and 180 degrees')
        return value
    
    @validates('latitude')
    def validate_latitude(self, value):
        if not -90 <= value <= 90:
            raise ValidationError('Latitude must be between -90 and 90 degrees')
        return value
    
    @validates('description')
    def validate_description(self, value):
        if not len(value) >= 10:
            raise ValidationError('Description must be at least 10 characters')
        return value

class LocationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model: Location
        load_instance = True
        sqla_session = db.session
        include_relationships = True

location_schema = LocationSchema()
locations_schema = LocationSchema(many=True)