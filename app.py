# -------------------------------------------------------------------------------> Imports
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import select

class Base(DeclarativeBase):
    pass
# -------------------------------------------------------------------------------> Instances
db = SQLAlchemy(model_class=Base)
ma = Marshmallow()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# -------------------------------------------------------------------------------> Initialize
db.init_app(app)
ma.init_app(app)
# -------------------------------------------------------------------------------> Junction Tables
mechanic_ticket = db.Table(
    "mechanic_ticket",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)

service_ticket = db.Table(
    "service_ticket",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("tickets.id")),
    db.Column("service_id", db.ForeignKey("services.id"))
)
# -------------------------------------------------------------------------------> Models
# -------------------------------------------------------------------------------> Models Customers
class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(16), nullable=False)

    customer_ticket: Mapped[list['Ticket']] = db.relationship(back_populates="customer")
# -------------------------------------------------------------------------------> Models Mechanics
class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(16), nullable=False)
    address: Mapped[str] = mapped_column(db.String(350), nullable=False)
    title: Mapped[str] = mapped_column(db.String(50), nullable=False)
    salary: Mapped[float] = mapped_column(nullable=False)

    mechanic_tickets: Mapped[list['Ticket']] = db.relationship("Ticket", secondary=mechanic_ticket, back_populates="mechanics")
# -------------------------------------------------------------------------------> Models Tickets
class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date] = mapped_column(nullable=False)
    vin: Mapped[str] = mapped_column(db.String(18), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))

    customer: Mapped['Customer'] = db.relationship(back_populates="customer_ticket")
    mechanics: Mapped[list['Mechanic']] = db.relationship("Mechanic", secondary=mechanic_ticket, back_populates="mechanic_tickets")
    services: Mapped[list['Service']] = db.relationship("Service", secondary=service_ticket, back_populates="service_tickets")
# -------------------------------------------------------------------------------> Models Services
class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_desc: Mapped[str] = mapped_column(db.String(100), nullable=False)

    service_tickets: Mapped[list['Ticket']] = db.relationship("Ticket", secondary=service_ticket, back_populates="services")
# -------------------------------------------------------------------------------> Schemas
# -------------------------------------------------------------------------------> Schema Customer
class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
# -------------------------------------------------------------------------------> Route
# -------------------------------------------------------------------------------> Create Customer
@app.route('/customers', methods=['POST'])
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
# -------------------------------------------------------------------------------> Get All Customers
@app.route('/customers', methods=['GET'])
def get_customers():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers_schema.jsonify(customers), 200
# -------------------------------------------------------------------------------> Get Customer By ID
@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer_id(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        return customer_schema.jsonify(customer), 200
    return jsonify({"error": "Customer does not exist"})
# -------------------------------------------------------------------------------> Update Customer
@app.route('/customers/<int:customer_id>', methods=['PUT'])
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
# -------------------------------------------------------------------------------> Delete Customer
@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):

    customer = db.session.get(Customer, customer_id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify(f"Deleted Customer: {customer.name}"), 200
    return jsonify({"error": "Customer does not exist"})
# -------------------------------------------------------------------------------> run
with app.app_context():
    # db.drop_all()
    db.create_all()
    

app.run(debug=True)

