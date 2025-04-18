from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from app.models import Mechanic, db
from app.extensions import limiter
# -------------------------------------------------------------------------------> Create Mechanic Route
@mechanics_bp.route('/', methods=['POST'])
@limiter.limit("50/day")
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    mechanic = db.session.execute(query).scalars().first()

    if not mechanic:
        new_mechanic = Mechanic(**mechanic_data)
        db.session.add(new_mechanic)
        db.session.commit()
        return mechanic_schema.jsonify(new_mechanic), 201
    return jsonify({"error": "Email already exists."}), 400
# -------------------------------------------------------------------------------> Get All Mechanics Route
@mechanics_bp.route('/', methods=['GET'])
def get_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()
    return mechanics_schema.jsonify(mechanics), 200
# -------------------------------------------------------------------------------> Get Mechanics By ID Route
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic_id(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Mechanic does not exist."})
# -------------------------------------------------------------------------------> Update Mechanic Route
@mechanics_bp.route('/<int:mechanic_id>', methods=['PUT'])
@limiter.limit("1/15 days")
def update_mechanic(mechanic_id):
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic:
        for field, value in mechanic_data.items():
            setattr(mechanic, field, value)
        db.session.commit()
        return mechanic_schema.jsonify(mechanic)
    return jsonify({"error:" "Customer ID does not exist."})
# -------------------------------------------------------------------------------> Delete Mechanic Route
@mechanics_bp.route('/<int:mechanic_id>', methods=['DELETE'])
@limiter.limit("5/day")
def delete_mechanic(mechanic_id):

    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic:
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify(f"Deleted Mechanic: {mechanic.name}"), 200
    return jsonify({"error": "Customer does not exist."})