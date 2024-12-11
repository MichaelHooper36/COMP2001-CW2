# features.py

from flask import abort, make_response

from config import db
from models import Feature, feature_schema, features_schema

def create(feature):
    trail_feature = feature.get("trail_feature")
    existing_feature = Feature.query.filter(Feature.trail_feature == trail_feature).one_or_none()

    if existing_feature is None:
        new_feature = feature_schema.load(feature, session=db.session)
        db.session.add(new_feature)
        db.session.commit()
        return feature_schema.dump(new_feature), 201
    else:
        abort(406, f"Feature with the name {trail_feature} already exists")

def read_one(trail_feature):
    feature = Feature.query.filter(Feature.trail_feature == trail_feature).one_or_none()

    if feature is not None:
        return feature_schema.dump(feature)
    else:
        abort(404, f"Feature with the name {trail_feature} not found")

def read_all():
    features = Feature.query.all()
    return features_schema.dump(features)


def update(trail_feature, feature):
    existing_featue = Feature.query.filter(Feature.trail_feature == trail_feature).one_or_none()

    if existing_featue:
        update_feature = feature_schema.load(feature, session=db.session)
        existing_featue.trail_feature = update_feature.trail_feature
        db.session.merge(existing_featue)
        db.session.commit()
        return feature_schema.dump(existing_featue), 201
    else:
        abort(404, f"Feature with the name {trail_feature} not found")

def delete(trail_feature):
    existing_feature = Feature.query.filter(Feature.trail_feature == trail_feature).one_or_none()

    if existing_feature:
        db.session.delete(existing_feature)
        db.session.commit()
        return make_response(f"{trail_feature} successfully deleted", 200)
    else:
        abort(404, f"Feature with the name {trail_feature} not found")

