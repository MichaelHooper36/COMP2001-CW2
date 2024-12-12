# trail_features.py

from flask import abort, make_response, request

from config import db
from models import Trail_Features, trail_feat_schema, trail_feats_schema

def create():
    trail_data = request.get_json()
    new_trail = trail_feat_schema.load(trail_data, session=db.session)
    db.session.add(new_trail)
    db.session.commit()
    return trail_feat_schema.dump(new_trail), 201

def read_one(id, type):
    if type == 'trail':
        attribute = 'trail_id'
    elif type == 'trail_feature':
        attribute = 'trail_feature_id'
    
    trail_feature = Trail_Features.query.filter(getattr(Trail_Features, attribute) == id).all()
    if trail_feature:
        return trail_feats_schema.dump(trail_feature)
    else:
        abort(404, "No trail feature found for the given ID")

def read_all():
    trail_feats = Trail_Features.query.all()
    return trail_feats_schema.dump(trail_feats)

def delete():
    data = request.get_json()
    trail_id = data.get('trail_id')
    feature_id = data.get('trail_feature_id')
    delete_all = data.get('delete_all', False)

    if not trail_id or not feature_id:
        abort(400, "Both 'trail_id' and 'trail_feature_id' are required")

    if delete_all:  
        existing_trail_features = Trail_Features.query.filter(Trail_Features.trail_id == trail_id).all()
        if existing_trail_features:
            for feature in existing_trail_features:
                db.session.delete(feature)
            db.session.commit()
            return make_response(f"All features tied to trail ID {trail_id} have been deleted", 204)
        else:
            abort(404, f"No features found linked to trail ID {trail_id}")
    else:  
        existing_trail_feature = Trail_Features.query.filter(Trail_Features.trail_id == trail_id,Trail_Features.trail_feature_id == feature_id).one_or_none()
        if existing_trail_feature:
            db.session.delete(existing_trail_feature)
            db.session.commit()
            return make_response(f"Feature ID {feature_id} tied to the trail ID {trail_id} has been deleted", 204)
        else:
            abort(404, f"Feature ID {feature_id} tied to the trail ID {trail_id} not found")
