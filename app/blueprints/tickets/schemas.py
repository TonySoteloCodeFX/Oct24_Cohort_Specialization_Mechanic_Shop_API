from app.extensions import ma
from app.models import Ticket
# -------------------------------------------------------------------------------> Schema Ticket
class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Ticket
        fields= ('mechanic_id', 'service_date', 'vin', 'customer_id')

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)