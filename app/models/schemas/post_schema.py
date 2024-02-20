from app.extensions import ma
from app.models.tables.post import Post
from app.models.schemas.user_schema import UserSchema
from app.models.schemas.comments_schema import CommentSchema

class PostSchema(ma.SQLAlchemyAutoSchema):
    owner_info = ma.Nested(UserSchema)
    comments = ma.Nested(CommentSchema, many=True)
    class Meta:
        model = Post
        load_instance = True
