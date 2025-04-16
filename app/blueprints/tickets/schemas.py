from app.extensions import ma
from app.models import Ticket
from typing import List
# -------------------------------------------------------------------------------> Schema Ticket
class TicketSchema(ma.SQLAlchemyAutoSchema):
    mechanic_ids = ma.List(ma.Integer(), load_only=True)

    class Meta:
        model = Ticket
        fields = ('service_date', 'vin', 'customer_id', 'mechanic_ids')


ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)