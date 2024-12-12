# users.py

from flask import abort, make_response, request

from config import db
from models import User, user_schema, people_schema

def create():
    user = request.get_json()
    user_id = user.get("user_id")
    existing_user = User.query.filter(User.user_id == user_id).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"Person with the user_id {user_id} already exists")

def read_one(user_id):
    user = User.query.filter(User.user_id == user_id).one_or_none()

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(404, f"Person with the user_id {user_id} not found")

def read_all():
    users = User.query.all()
    return people_schema.dump(users)


def update(user_id):
    user = request.get_json()
    existing_user = User.query.filter(User.user_id == user_id).one_or_none()

    if existing_user:
        update_person = user_schema.load(user, session=db.session)
        existing_user.user_id = update_person.user_id
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 201
    else:
        abort(404, f"Person with the user_id {user_id} not found")

def delete(user_id):
    existing_user = User.query.filter(User.user_id == user_id).one_or_none()

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"{user_id} successfully deleted", 200)
    else:
        abort(404, f"Person with the user_id {user_id} not found")

