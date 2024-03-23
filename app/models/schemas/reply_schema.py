from app.extensions import ma
from app.models.tables.reply import Reply

class ReplySchema(ma.SQLAlchemyAutoSchema):
    owner = ma.Nested('UserSchema')
    class Meta:
        model = Reply
        load_instance = True
