from app.extensions import ma
from app.models.tables.user import User
from app.models.schemas.user_type_schema import UserTypeSchema

class UserSchema(ma.SQLAlchemyAutoSchema):
    user_type = ma.Nested(UserTypeSchema)
    
    class Meta:
        model = User
        load_instance = True
        exclude = ['password_hash']
