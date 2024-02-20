from app.extensions import ma
from app.models.tables.user_type import UserType


class UserTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserType
        load_instance = True
