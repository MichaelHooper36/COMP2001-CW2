# locations.py

from flask import abort, make_response, request

from config import db
from models import Location, location_schema, locations_schema

def create(location):
    longitude = location.get("longitude")
    latitude = location.get("latitude")
    existing_location = Location.query.filter(Location.longitude == longitude, Location.latitude == latitude).one_or_none()

    if existing_location is None:
        new_location = location_schema.load(location, session=db.session)
        db.session.add(new_location)
        db.session.commit()
        return location_schema.dump(new_location), 201
    else:
        abort(406, f"Location with the coordinates {longitude, latitude} already exists")

def read_one(longitude, latitude):
    location = Location.query.filter(Location.longitude == longitude, Location.latitude == latitude).one_or_none()

    if location is not None:
        return location_schema.dump(location)
    else:
        abort(404, f"Place with the coordinates {longitude, latitude} not found")

def read_all():
    locations = Location.query.all()
    return locations_schema.dump(locations)

def update(location_id):
    location_data = request.get_json()
    existing_location = Location.query.filter(Location.location_id == location_id).one_or_none()

    if existing_location:
        if 'longitude' in location_data:
            existing_location.longitude = location_data['longitude']
        if 'latitude' in location_data:
            existing_location.latitude = location_data['latitude']
        if 'description' in location_data:
            existing_location.description = location_data['description']
        
        db.commit()
        return make_response(f"Location with ID {location_id} has been updated successfully.", 200)
    else:
        abort(404, f"Location with ID {location_id} not found.")

def delete(longitude, latitude):
    existing_location = Location.query.filter(Location.longitude == longitude, Location.latitude == latitude).one_or_none()

    if existing_location:
        db.session.delete(existing_location)
        db.session.commit()
        return make_response(f"{longitude, latitude} successfully deleted", 200)
    else:
        abort(404, f"Place with the coordinates {longitude, latitude} not found")