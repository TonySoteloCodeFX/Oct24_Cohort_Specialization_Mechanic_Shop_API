# -------------------------------------------------------------------------------> Imports
from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import customers_bp
from .schemas import customer_schema, customers_schema
from app.models import Customer, db
from app.extensions import limiter, cache
# -------------------------------------------------------------------------------> Create Customer Route
@customers_bp.route('/', methods=['POST'])
@limiter.limit("12/day")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    customer = db.session.execute(query).scalars().first()

    if not customer:
        new_customer = Customer(**customer_data)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer), 201
    return jsonify({"error": "Email already exists."}), 400
# -------------------------------------------------------------------------------> Get All Customers Route
@customers_bp.route('/', methods=['GET'])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200
# -------------------------------------------------------------------------------> Get Customer By ID Route
@customers_bp.route('/<int:customer_id>', methods=['GET'])
@cache.cached(timeout=30)
def get_customer_id(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer does not exist"})
# -------------------------------------------------------------------------------> Update Customer Route
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit("1/19 days")
def update_customer(customer_id):
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer = db.session.get(Customer, customer_id)

    if customer:
        for field, value in customer_data.items():
            setattr(customer, field, value)
        db.session.commit()
        return customer_schema.jsonify(customer)
    return jsonify({"error:" "Customer ID does not exist."})
# -------------------------------------------------------------------------------> Delete Customer Route
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@limiter.limit("5/day")
def delete_customer(customer_id):

    customer = db.session.get(Customer, customer_id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify(f"Deleted Customer: {customer.name}"), 200
    return jsonify({"error": "Customer does not exist"})