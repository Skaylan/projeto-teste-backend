from flask import Flask

app = Flask(__name__)


from app.controllers import routes
from app.models.tables.user import User
from app.models.tables.user_type import UserType
from app.models.tables.post import Post
from app.models.tables.comment import Comment
