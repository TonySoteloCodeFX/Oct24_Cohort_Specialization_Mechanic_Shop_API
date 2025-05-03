from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import tickets_bp
from .schemas import ticket_schema, tickets_schema
from app.blueprints.serial_items.schemas import serial_items_schema
from app.models import Ticket, db, Mechanic, Service, SerialItem
from app.extensions import limiter, cache
# -------------------------------------------------------------------------------> Create Ticket Route
@tickets_bp.route('/', methods=['POST'])
@limiter.limit("20/hour")
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
# -------------------------------------------------------------------------------> Update Ticket Route
@tickets_bp.route('/<int:ticket_id>', methods=['PUT'])
@limiter.limit("2/hour")
def update_ticket(ticket_id):
    try:
        ticket_data = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    ticket = db.session.get(Ticket, ticket_id)

    if not ticket:
        return jsonify({"error": "Ticket ID does not exist."})
    
    ticket.service_date = ticket_data.get("service_date", ticket.service_date)
    ticket.vin = ticket_data.get("vin", ticket.vin)
    ticket.customer_id = ticket_data.get("customer_id", ticket.customer_id)

    if "mechanic_ids" in ticket_data:
        ticket.mechanics = []
        for mechanic_id in ticket_data["mechanic_ids"]:
            query = select(Mechanic).where(Mechanic.id == mechanic_id)
            mechanic = db.session.execute(query).scalar()
            if mechanic:
                ticket.mechanics.append(mechanic)
            else:
                return jsonify({"Message": f"Invalid mechanic ID: {mechanic_id}"}), 400
            
    if "service_ids" in ticket_data:
        ticket.services = []
        for service_id in ticket_data["service_ids"]:
            query = select(Service).where(Service.id == service_id)
            service = db.session.execute(query).scalar()
            if service:
                ticket.services.append(service)
            else:
                return jsonify({"Messages": f"Invalid service ID: {service_id}"}), 400
    
    db.session.commit()
    return ticket_schema.jsonify(ticket), 200
# -------------------------------------------------------------------------------> Delete Ticket Route
@tickets_bp.route('/<int:ticket_id>', methods=['DELETE'])
@limiter.limit("5/day")
def delete_ticket(ticket_id):
    ticket = db.session.get(Ticket, ticket_id)

    if ticket:
        db.session.delete(ticket)
        db.session.commit()
        return jsonify(f"Deleted Ticket: {ticket_id}"), 200
    return jsonify({"error": "Ticket does not exist."}), 400
# -------------------------------------------------------------------------------> Add Item to Ticket Route
@tickets_bp.route("/<int:ticket_id>/add_item/<int:description_id>", methods=['PUT'])
def add_item(ticket_id, description_id):
    ticket = db.session.get(Ticket, ticket_id)
    query = select(SerialItem).where(SerialItem.description.has(id = description_id), SerialItem.ticket_id == None)
    item = db.session.execute(query).scalars().first()

    if not item:
        return jsonify({"error": "Item out of stock."}), 400
    
    if ticket:
        item.ticket_id = ticket_id
        db.session.commit()
        return jsonify({
            "message": f"Successfully added {item.description.name} to ticket",
            'Ticket': ticket_schema.dump(ticket),
            'Items': serial_items_schema.dump(ticket.ticket_items)
        })
    return jsonify({"error": "Ticket does not exist."}), 400