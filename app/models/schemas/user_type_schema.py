from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.user_type import UserType


class UserTypeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserType
        load_instance = True
