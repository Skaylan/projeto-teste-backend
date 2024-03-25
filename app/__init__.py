import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import *
from app.controllers.routes.social_media_routes import social_media_route
from app.controllers.routes.user_routes import user_route
from app.controllers.routes.routes_for_testing import route_for_testing
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
    app.register_blueprint(social_media_route)
    app.register_blueprint(route_for_testing)
    app.register_blueprint(auth_route)
    app.register_blueprint(friend_route)
    
    
    
    return app