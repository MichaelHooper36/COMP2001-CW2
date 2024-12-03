# users.py

from flask import abort, make_response

from config import db
from models import Person, people_schema, person_schema

def create(person):
    name = person.get("name")
    existing_person = Person.query.filter(Person.name == name).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(406, f"Person with the name {name} already exists")

def read_one(name):
    person = Person.query.filter(Person.name == name).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with the name {name} not found")

def read_all():
    people = Person.query.all()
    return person_schema.dump(people)


def update(name, person):
    existing_person = Person.query.filter(Person.name == name).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with the name {name} not found")

def delete(name):
    existing_person = Person.query.filter(Person.lname == name).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{name} successfully deleted", 200)
    else:
        abort(404, f"Person with the name {name} not found")

