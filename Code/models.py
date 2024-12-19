# models.py

from marshmallow import validates, ValidationError, fields

from config import db, ma

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'schema': 'CW2'}
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(63), unique=True)
    email = db.Column(db.String(63), unique=True)
    password = db.Column(db.String(63))
    role = db.Column(db.String(5))

    @validates('email')
    def validate_model(self, value):
        import re
        if not re.match(r"^[^@]+@[^@]+\.[^@]{2,}$", value):
            raise ValidationError('Invalid email address format')
        else:
            return value

    @validates('role')
    def validate_role(self, value):
        if value not in ['admin', 'user']:
            raise ValidationError('Invalid role')
        else:
            return value

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

class Feature(db.Model):
    __tablename__ = "features"
    __table_args__ = {'schema': 'CW2'}
    trail_feature_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_feature = db.Column(db.String(31), unique=True)

class FeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model: Feature
        load_instance = True
        sqla_session = db.session
        include_relationships = True

feature_schema = FeatureSchema()
features_schema = FeatureSchema(many=True)

class Trail(db.Model):
    __tablename__ = "trails"
    __table_args__ = {'schema': 'CW2'}
    trail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trail_name = db.Column(db.String(127))
    trail_summary = db.Column(db.String(500))
    trail_description = db.Column(db.String(500))
    difficulty = db.Column(db.String(8))
    location = db.Column(db.String(63))
    length = db.Column(db.Float)
    elevation_gain = db.Column(db.Integer)
    route_type = db.Column(db.String(15))
    owner_id = db.Column(db.Integer, db.ForeignKey('CW2.users.user_id'))

    LOCATION_ID = 'CW2.location_point.location_id'
    location_point_1 = db.Column(db.Integer, db.ForeignKey(LOCATION_ID))
    location_point_2 = db.Column(db.Integer, db.ForeignKey(LOCATION_ID))
    location_point_3 = db.Column(db.Integer, db.ForeignKey(LOCATION_ID))
    location_point_4 = db.Column(db.Integer, db.ForeignKey(LOCATION_ID))
    location_point_5 = db.Column(db.Integer, db.ForeignKey(LOCATION_ID))

    owner = db.relationship("User", backref = "trails")
    location_1 = db.relationship("Location", foreign_keys=[location_point_1])
    location_2 = db.relationship("Location", foreign_keys=[location_point_2])
    location_3 = db.relationship("Location", foreign_keys=[location_point_3])
    location_4 = db.relationship("Location", foreign_keys=[location_point_4])
    location_5 = db.relationship("Location", foreign_keys=[location_point_5])

    @validates('difficulty')
    def validate_difficulty(self, value):
        if value not in ['easy', 'moderate', 'hard']:
            raise ValidationError('Difficulty must be either easy, moderate or hard')
        else:
            return value
    
    @validates('length')
    def validate_length(self, value):
        value = round(value, 2)
        if not value >0:
            raise ValidationError('Length must be positive')
        else:
            return value
    
    @validates('elevation_gain')
    def validate_elevation(self, value):
        if not value >=0:
            raise ValidationError('Elevation gained must not be negative')
        else:
            return value
    
    @validates('route_type')
    def validate_route_type(self, value):
        if value not in ['loop', 'out and back', 'point to point']:
            raise ValidationError("Route type must be either loop, out and back, or point to point")
        else:
            return value

class TrailSchema(ma.SQLAlchemyAutoSchema):
    trail_id = fields.Integer(required=True)
    trail_name = fields.Str(required=True)
    trail_summary = fields.Str()
    trail_description = fields.Str()
    location = fields.Str()
    difficulty = fields.Str()
    elevation_gain = fields.Integer(missing=None)  
    route_type = fields.Str()  
    owner_id = fields.Integer(required=True)
    location_point_1 = fields.Integer()
    location_point_2 = fields.Integer()
    location_point_3 = fields.Integer()
    location_point_4 = fields.Integer()
    location_point_5 = fields.Integer()
    class Meta:
        model = Trail
        load_instance = True
        sqla_session = db.session

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)

class Trail_Features(db.Model):
    __tablename__ = "trail_features"
    _table_args__ = {'schema': 'CW2'}
    trail_id = db.Column(db.Integer, db.ForeignKey('CW2.trails.trail_id'), primary_key=True)
    trail_feature_id = db.Column(db.Integer, db.ForeignKey('CW2.features.trail_feature_id'), primary_key=True)

    trail = db.relationship("Trail", backref = "trail_features")
    trail_feature = db.relationship("Feature", backref = "trail_features")

class TrailFeatureSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model: Trail_Features
        load_instance = True
        sqla_session = db.session
        include_relationships = True

trail_feat_schema = TrailFeatureSchema()
trail_feats_schema = TrailFeatureSchema(many=True)