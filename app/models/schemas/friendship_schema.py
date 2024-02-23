from app.models.tables.friendship import Friendship
# from app.models.schemas.user_schema import UserSchema
from app.extensions import ma

class FriendshipSchema(ma.SQLAlchemyAutoSchema):
  friend = ma.Nested('UserSchema')
  
  class Meta:
    model = Friendship
    load_instance = True
    fields = ('id', 'user_id', 'friend_id', 'friend')