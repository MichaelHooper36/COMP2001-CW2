# trails.py

from flask import abort, make_response, request

from config import db
from models import Trail, trail_schema, trails_schema
from models import Trail_Features

def create():
    trail_data = request.get_json()
    new_trail = trail_schema.load(trail_data, session=db.session)
    db.session.add(new_trail)
    db.session.commit()
    return trail_schema.dump(new_trail), 201

def read_one(trail_id):
    trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if trail is not None:
        return trail_schema.dump(trail)
    else:
        abort(404, f"Trail with the ID {trail_id} not found")

def read_all():
    trails = db.session.query(Trail).all()
    return trails_schema.dump(trails)


def update(trail_id):
    trail_data = request.get_json()
    existing_trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()

    if existing_trail:
        if 'trail_name' in trail_data:
            existing_trail.trail_name = trail_data['trail_name']
        if 'trail_summary' in trail_data:
            existing_trail.trail_summary = trail_data['trail_summary']
        if 'trail_description' in trail_data:
            existing_trail.trail_description = trail_data['trail_description']
        if 'difficulty' in trail_data:
            existing_trail.difficulty = trail_data['difficulty']
        if 'location' in trail_data:
            existing_trail.location = trail_data['location']
        if 'length' in trail_data:
            existing_trail.length = trail_data['length']
        if 'elevation_gain' in trail_data:
            existing_trail.elevation_gain = trail_data['elevation_gain']
        if 'route_type' in trail_data:
            existing_trail.route_type = trail_data['route_type']
        if 'owner_id' in trail_data:
            existing_trail.owner_id = trail_data['owner_id']
        if 'location_point_1' in trail_data:
            existing_trail.location_point_1 = trail_data['location_point_1']
        if 'location_point_2' in trail_data:
            existing_trail.location_point_2 = trail_data['location_point_2']
        if 'location_point_3' in trail_data:
            existing_trail.location_point_3 = trail_data['location_point_3']
        if 'location_point_4' in trail_data:
            existing_trail.location_point_4 = trail_data['location_point_4']
        if 'location_point_5' in trail_data:
            existing_trail.location_point_5 = trail_data['location_point_5']
        
        db.commit()
        return make_response(f"Trail with name {existing_trail.trail_name} has been updated successfully.", 200)
    else:
        abort(404, f"Trail with ID {trail_id} not found.")

def delete(trail_id):
    existing_trail = Trail.query.filter(Trail.trail_id == trail_id).one_or_none()
    existing_trail_features = Trail_Features.query.filter(Trail_Features.trail_id == trail_id).all()

    if existing_trail:
        for trail_feature in existing_trail_features:
            db.session.delete(trail_feature)
        db.session.delete(existing_trail)
        db.session.commit()
        return make_response(f"{existing_trail.trail_name} successfully deleted", 200)
    else:
        abort(404, f"Trail with the ID {trail_id} not found")

