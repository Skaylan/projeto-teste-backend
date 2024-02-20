import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from .extensions import *
from app.controllers.post_routes.routes import post_route
from app.controllers.user_routes.routes import user_route
from app.controllers.test_routes.routes import test_route
from app.controllers.auth_routes.routes import auth_route


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
    
    
    return app