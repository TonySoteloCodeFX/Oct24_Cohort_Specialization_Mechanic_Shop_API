from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import tickets_bp
from .schemas import ticket_schema, tickets_schema
from app.models import Ticket, db
# -------------------------------------------------------------------------------> Create Ticket Route
@tickets_bp.route('/', methods=['POST'])
def create_ticket():
    try:
        ticket_data = ticket_schema.load(request.json)
        print(ticket_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    return jsonify({"Message": "Nice Work"})