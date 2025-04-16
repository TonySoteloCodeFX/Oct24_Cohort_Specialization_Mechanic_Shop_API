from app.extensions import ma
from app.models import Ticket, Mechanic, Customer, Service
from marshmallow import fields

# -------------------------------------------------------------------------------> Mechanic Schema 
class MechanicNestedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        fields = ('id', 'name')
# -------------------------------------------------------------------------------> Service Schema
class ServiceNestedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service
        fields = ('id', 'service_desc',)
# -------------------------------------------------------------------------------> Customer Schema
class CustomerNestedSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer
        fields = ('id', 'name')
# -------------------------------------------------------------------------------> Ticket Schema
class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanic_ids = ma.List(ma.Integer(), load_only=True)
    mechanics = ma.Nested(MechanicNestedSchema, many=True, dump_only=True)

    service_ids = ma.List(ma.Integer(), load_only=True)
    services = ma.Nested(ServiceNestedSchema, many=True, dump_only=True)

    customer = ma.Nested(CustomerNestedSchema, dump_only=True)
    customer_id = fields.Integer(load_only=True)

    class Meta:
        model = Ticket
        fields = ('id', 'service_date', 'vin', 'customer', 'customer_id', 'mechanic_ids', 'mechanics', 'service_ids', 'services')

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)