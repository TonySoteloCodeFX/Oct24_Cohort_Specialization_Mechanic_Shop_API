from app.extensions import ma
from app.models import Mechanic

# -------------------------------------------------------------------------------> Schema Mechanic
class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
# -------------------------------------------------------------------------------> Schema Mechanic Activity Tracker
class MechanicActivitySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanic
        include_relationships = True
        

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
login_schema = MechanicSchema(exclude=['id', 'name', 'phone', 'address', 'title', 'salary'])
mechanic_activity_schema = MechanicActivitySchema(many=True)