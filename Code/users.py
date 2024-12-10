# users.py

from flask import abort, make_response

from config import db
from models import User, user_schema, people_schema

def create(user):
    username = user.get("username")
    existing_user = User.query.filter(User.username == username).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"Person with the username {username} already exists")

def read_one(username):
    user = User.query.filter(User.username == username).one_or_none()

    if user is not None:
        return user_schema.dump(user)
    else:
        abort(404, f"Person with the username {username} not found")

def read_all():
    users = User.query.all()
    return people_schema.dump(users)


def update(username, user):
    existing_user = User.query.filter(User.username == username).one_or_none()

    if existing_user:
        update_person = user_schema.load(user, session=db.session)
        existing_user.username = update_person.username
        db.session.merge(existing_user)
        db.session.commit()
        return user_schema.dump(existing_user), 201
    else:
        abort(404, f"Person with the username {username} not found")

def delete(username):
    existing_user = User.query.filter(User.username == username).one_or_none()

    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()
        return make_response(f"{username} successfully deleted", 200)
    else:
        abort(404, f"Person with the username {username} not found")

