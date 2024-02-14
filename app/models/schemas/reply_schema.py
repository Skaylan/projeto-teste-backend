from app.config.app_config import *
from app.config.db_config import *
from app.models.tables.reply import Reply

class ReplySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Reply
        load_instance = True
