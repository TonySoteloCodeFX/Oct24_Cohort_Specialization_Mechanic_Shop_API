from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import services_bp
from .schemas import service_schema, services_schema
from app.models import Service, db
from app.extensions import limiter, cache
# -------------------------------------------------------------------------------> Create Service Route
@services_bp.route('/', methods=['POST'])
@limiter.limit("20/day")
def create_service():
    try:
        service_data = service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Service).where(Service.service_desc == service_data['service_desc'])
    service = db.session.execute(query).scalars().first()

    if not service:
        new_service = Service(**service_data)
        db.session.add(new_service)
        db.session.commit()
        return service_schema.jsonify(new_service), 201
    return jsonify({"error": "Service already exists."}), 400
# -------------------------------------------------------------------------------> Get All Services Route
@services_bp.route('/', methods=['GET'])
@cache.cached(timeout=30)
def get_services():
    query = select(Service)
    services = db.session.execute(query).scalars().all()
    return services_schema.jsonify(services), 200
# -------------------------------------------------------------------------------> Get Service By ID Route
@services_bp.route('/<int:service_id>', methods=['GET'])
@cache.cached(timeout=30)
def get_service_id(service_id):
    service = db.session.get(Service, service_id)

    if service:
        return service_schema.jsonify(service), 200
    return jsonify({"error": "Service does not exist."})
# -------------------------------------------------------------------------------> Update Service Route
@services_bp.route('/<int:service_id>', methods=['PUT'])
@limiter.limit("1/day")
def update_service(service_id):
    try:
        service_data = service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    service = db.session.get(Service, service_id)

    if service:
        for field, value in service_data.items():
            setattr(service, field, value)
        db.session.commit()
        return service_schema.jsonify(service)
    return jsonify({"error": "Service ID does not exist."})
# -------------------------------------------------------------------------------> Delete Service Route
@services_bp.route('/<int:service_id>', methods=['DELETE'])
@limiter.limit("5/day")
def delete_service(service_id):

    service = db.session.get(Service, service_id)

    if service:
        db.session.delete(service)
        db.session.commit()
        return jsonify(f"Deleted Service: {service.service_desc}"), 200
    return jsonify({"error": "Service does not exist."})