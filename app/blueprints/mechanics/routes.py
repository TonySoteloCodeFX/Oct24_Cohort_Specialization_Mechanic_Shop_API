from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema
from app.models import Mechanic, db
# -------------------------------------------------------------------------------> Create Mechanic Route