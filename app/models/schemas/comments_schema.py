from app.extensions import ma
from app.models.tables.comment import Comment
from app.models.schemas.user_schema import UserSchema

class CommentSchema(ma.SQLAlchemyAutoSchema):
    owner = ma.Nested(UserSchema)
    class Meta:
        model = Comment
        load_instance = True
        fields = (
          'id', 
          'post_id', 
          'reply_id', 
          'owner_id', 
          'comment', 
          'created_at', 
          'updated_at', 
          'owner'
        )
