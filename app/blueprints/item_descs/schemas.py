from app.extensions import ma
from app.models import ItemDesc

# -------------------------------------------------------------------------------> Schema Item Description
class ItemDescSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemDesc

itemdesc_schema = ItemDescSchema()
itemdescs_schema = ItemDescSchema(many=True)