from app.extensions import ma
from app.models import Service

# -------------------------------------------------------------------------------> Schema Service
class ServiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Service

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)