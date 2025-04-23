from flask import Blueprint

serial_item_bp = Blueprint("serial_item_bp", __name__)

from . import routes