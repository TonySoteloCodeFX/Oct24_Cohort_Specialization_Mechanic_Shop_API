from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import item_descs_bp
from .schemas import itemdesc_schema, itemdescs_schema
from app.models import ItemDesc, db, SerialItem
from app.extensions import limiter, cache
# -------------------------------------------------------------------------------> Create Item Desc Route
@item_descs_bp.route('/', methods=['POST'])
@limiter.limit("12/day")
def create_item_desc():
    try:
        item_desc_data = itemdesc_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(ItemDesc).where(ItemDesc.name == item_desc_data['name'])
    item_desc = db.session.execute(query).scalars().first()

    if not item_desc:
        new_item_desc = ItemDesc(**item_desc_data)
        db.session.add(new_item_desc)
        db.session.commit()
        return itemdesc_schema.jsonify(new_item_desc), 201
    return jsonify({"error": "Item already exists."}), 400
# -------------------------------------------------------------------------------> Get All Item Desc Route
@item_descs_bp.route('/', methods=['GET'])
def get_item_descs():
    query = select(ItemDesc)
    item_descs = db.session.execute(query).scalars().all()
    return itemdescs_schema.jsonify(item_descs), 200
# -------------------------------------------------------------------------------> Get Item Desc By ID Route
@item_descs_bp.route('/<int:item_desc_id>', methods=['GET'])
@cache.cached(timeout=30)
def get_item_desc_id(item_desc_id):
    item_desc = db.session.get(ItemDesc, item_desc_id)

    if item_desc:
        return itemdesc_schema.jsonify(item_desc), 200
    return jsonify({"error": "Item does not exist"})
# -------------------------------------------------------------------------------> Update Item Desc Route
@item_descs_bp.route('/<int:item_desc_id>', methods=['PUT'])
# @limiter.limit("1/19 days")
def update_item_desc(item_desc_id):
    try:
        item_desc_data = itemdesc_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    item_desc = db.session.get(ItemDesc, item_desc_id)

    if item_desc:
        for field, value in item_desc_data.items():
            setattr(item_desc, field, value)
        db.session.commit()
        return itemdesc_schema.jsonify(item_desc)
    return jsonify({"error:" "Item does not exist."})
# -------------------------------------------------------------------------------> Delete Item Desc Route
@item_descs_bp.route('/<int:item_desc_id>', methods=['DELETE'])
# @limiter.limit("5/day")
def delete_item_desc(item_desc_id):

    item_desc = db.session.get(ItemDesc, item_desc_id)

    if item_desc:
        db.session.delete(item_desc)
        db.session.commit()
        return jsonify(f"Item Deleted: {item_desc.name}"), 200
    return jsonify({"error": "Item does not exist"})
# -------------------------------------------------------------------------------> Search Item Desc Inventory Route
@item_descs_bp.route('/search', methods=['GET'])
def search_item():

    name = request.args.get('item')
    
    query = select(ItemDesc).where(ItemDesc.name.ilike(f'%{name}%'))
    item_desc = db.session.execute(query).scalars().first()

    stock_query = select(SerialItem).where(
        SerialItem.description.has(name = item_desc.name), 
        SerialItem.ticket_id == None)
    stock = len(db.session.execute(stock_query).scalars().all())

    if item_desc:
        return jsonify({
            'item': itemdesc_schema.dump(item_desc),
            'stock': stock
        })
    return jsonify({"error": "No items match this search."}), 404



