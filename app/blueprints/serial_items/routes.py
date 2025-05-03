from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import serial_item_bp
from .schemas import serial_item_schema, serial_items_schema
from app.models import ItemDesc, SerialItem, db
from app.extensions import limiter, cache
# -------------------------------------------------------------------------------> Create Serial Item Route
@serial_item_bp.route('/<int:description_id>', methods=['POST'])
def create_serial_item(description_id):
    item_desc = db.session.get(ItemDesc, description_id)
    
    if item_desc:
        new_serial_item = SerialItem(description_id = description_id)
        db.session.add(new_serial_item)
        db.session.commit()
        return serial_item_schema.jsonify(new_serial_item), 201
    return jsonify({"error": f"Invalid {description_id}"})
# -------------------------------------------------------------------------------> Get All Serial Items Route
@serial_item_bp.route('/', methods=['GET'])
def get_serial_item():
    query = select(SerialItem)
    item_descs = db.session.execute(query).scalars().all()
    return serial_items_schema.jsonify(item_descs), 200
# -------------------------------------------------------------------------------> Delete Serial Item Route
@serial_item_bp.route('/<int:serial_item_id>', methods=['DELETE'])
# @limiter.limit("5/day")
def delete_serial_item(serial_item_id):
    serial_item = db.session.get(SerialItem, serial_item_id)

    if serial_item:
        item_name = serial_item.description.name
        db.session.delete(serial_item)
        db.session.commit()
        return jsonify(f'Deleted Item: {item_name}, Serial Number: {serial_item_id}'), 200
    
    return jsonify({"error": "Serial ID does not exist."}), 404