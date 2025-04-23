from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import date
from typing import List
# -------------------------------------------------------------------------------> Base Model
class Base(DeclarativeBase):
    pass
# -------------------------------------------------------------------------------> Initialize
db = SQLAlchemy(model_class=Base)
# -------------------------------------------------------------------------------> Junction Table Mechanic Ticket
mechanic_ticket = db.Table(
    "mechanic_ticket",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("tickets.id")),
    db.Column("mechanic_id", db.ForeignKey("mechanics.id"))
)
# -------------------------------------------------------------------------------> Junction Table Service Ticket
service_ticket = db.Table(
    "service_ticket",
    Base.metadata,
    db.Column("ticket_id", db.ForeignKey("tickets.id")),
    db.Column("service_id", db.ForeignKey("services.id"))
)
# -------------------------------------------------------------------------------> Models Customers
class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(16), nullable=False)

    customer_ticket: Mapped[List['Ticket']] = db.relationship(back_populates="customer")
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
    password: Mapped[str] = mapped_column(nullable=False)

    mechanic_tickets: Mapped[List['Ticket']] = db.relationship("Ticket", secondary=mechanic_ticket, back_populates="mechanics")
# -------------------------------------------------------------------------------> Models Tickets
class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_date: Mapped[date] = mapped_column(nullable=False)
    vin: Mapped[str] = mapped_column(db.String(18), nullable=False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey("customers.id"))

    customer: Mapped['Customer'] = db.relationship(back_populates="customer_ticket")
    mechanics: Mapped[List['Mechanic']] = db.relationship("Mechanic", secondary=mechanic_ticket, back_populates="mechanic_tickets")
    services: Mapped[List['Service']] = db.relationship("Service", secondary=service_ticket, back_populates="service_tickets")
# -------------------------------------------------------------------------------> Models Services
class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_desc: Mapped[str] = mapped_column(db.String(100), nullable=False)

    service_tickets: Mapped[List['Ticket']] = db.relationship("Ticket", secondary=service_ticket, back_populates="services")
# -------------------------------------------------------------------------------> Model Item Descriptions
class ItemDesc(Base):
    __table__ = "item_descs"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.float, nullable=False)

    serial_items: Mapped[List['SerialItem']] = db.relationship(back_populates = 'description')
# -------------------------------------------------------------------------------> Model Serial Items
class SerialItem(Base):
    __table__ = "serial_items"
    id: Mapped[int] = mapped_column(primary_key= True)
    description_id: Mapped[int] = mapped_column(db.ForeignKey("item_descs.id"))
    ticket_id: Mapped[int] = mapped_column(db.ForeignKey("tickets.id"), nullable=True)

    description: Mapped[List['ItemDesc']] = db.relationship(back_populates = 'serial_items')