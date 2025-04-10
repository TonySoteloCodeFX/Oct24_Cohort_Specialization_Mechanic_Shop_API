# -------------------------------------------------------------------------------> Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

db.init_app(app)

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

    mechanic_tickets: Mapped[list['Ticket']] = db.relationship(back_populates="mechanics")

# -------------------------------------------------------------------------------> Models Tickets
class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date] = mapped_column(nullable=False)
    vin: Mapped[int] = mapped_column(db.String(18), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))
    service_id: Mapped[int] = mapped_column(db.ForeignKey("services.id"))

    customer: Mapped['Customer'] = db.relationship(back_populates="customer_ticket")
    mechanics: Mapped['Mechanic'] = db.relationship(back_populates="mechanic_tickets")
    service: Mapped['Service'] = db.relationship(back_populates="service_tickets")

# -------------------------------------------------------------------------------> Models Services
class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_desc: Mapped[str] = mapped_column(db.String(100), nullable=False)

    service_tickets: Mapped['Ticket'] = db.relationship(back_populates="service")



with app.app_context():
    db.create_all()
    # db.drop_all()

app.run(debug=True)

