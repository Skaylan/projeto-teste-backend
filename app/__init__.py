import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import *
from app.controllers.routes.post_routes import post_route
from app.controllers.routes.user_routes import user_route
from app.controllers.routes.test_routes import test_route
from app.controllers.routes.auth_routes import auth_route
from app.controllers.routes.friend_routes import friend_route


load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    app.register_blueprint(user_route)
    app.register_blueprint(post_route)
    app.register_blueprint(test_route)
    app.register_blueprint(auth_route)
    app.register_blueprint(friend_route)
    
    
    
    return app