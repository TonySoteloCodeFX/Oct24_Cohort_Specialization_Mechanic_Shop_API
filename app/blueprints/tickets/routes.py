from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import tickets_bp
from .schemas import ticket_schema, tickets_schema
from app.models import Ticket, db, Mechanic, Service
# -------------------------------------------------------------------------------> Create Ticket Route
@tickets_bp.route('/', methods=['POST'])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
        print(ticket_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = Ticket(service_date=ticket_data['service_date'], vin=ticket_data['vin'], customer_id=ticket_data['customer_id'])

    for mechanic_id in ticket_data["mechanic_ids"]:
        query = select(Mechanic).where(Mechanic.id==mechanic_id)
        mechanic = db.session.execute(query).scalar()
        if mechanic:
            new_ticket.mechanics.append(mechanic)
        else:
            return jsonify({"Message": "Invalid mechanic ID."}), 400
    
    for service_id in ticket_data["service_ids"]:
        query = select(Service).where(Service.id==service_id)
        service = db.session.execute(query).scalar()
        if service:
            new_ticket.services.append(service)
        else:
            return jsonify({"Message": "Invalid service ID."}), 400

    
    db.session.add(new_ticket)
    db.session.commit()

    return ticket_schema.jsonify(new_ticket), 201
# -------------------------------------------------------------------------------> Get All Tickets Route
@tickets_bp.route('/', methods=['GET'])
def get_tickets():
    query = select(Ticket)
    tickets = db.session.execute(query).scalars().all()
    return tickets_schema.jsonify(tickets), 200
# -------------------------------------------------------------------------------> Get Ticket by ID Route
@tickets_bp.route('/<int:ticket_id>', methods=['GET'])
def get_ticket_id(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if ticket:
        return ticket_schema.jsonify(ticket), 200
    return jsonify({"error": "Ticket does not exist"})
# -------------------------------------------------------------------------------> Update Ticket up Next
