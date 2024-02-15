from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.post import Post
from app.models.schemas.user_schema import UserSchema

class PostSchema(ma.SQLAlchemyAutoSchema):
    owner_info = ma.Nested(UserSchema)
    class Meta:
        model = Post
        load_instance = True
