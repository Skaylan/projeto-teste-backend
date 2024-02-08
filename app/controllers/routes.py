import os
import sys
from app import app
from flask import jsonify, request
from app.config.db_config import *
from app.config.app_config import *
from app.models.tables.user import User
from app.models.tables.user_type import UserType
from app.models.schemas.user_schema import UserSchema
from app.models.schemas.user_type_schema import UserTypeSchema
from werkzeug.security import generate_password_hash, check_password_hash

        
@app.route('/api/create_user', methods=['POST'])
def create_user():
    if request.method == 'POST':
        try:
            body = request.get_json()
            name = body.get('name')
            email = body.get('email')
            password = body.get('password')
            user_type_id = body.get('user_type_id')
            
            password_hash = generate_password_hash(password)
            
            user = User(name=name, email=email, password_hash=password_hash, user_type_id=user_type_id)
            db.session.add(user)
            db.session.commit()
            
            return jsonify({
                'message': "Usuario criado com sucesso!"
            }), 201
            
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500


@app.route('/api/get_users', methods=['GET'])
def get_users():
    if request.method == 'GET':
        try:   
            users = User.query.all()
            schema = UserSchema(many=True)
            payload = schema.dump(users)
            return jsonify({
                'users': payload
            }), 200
            
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500


@app.route('/api/create_user_type', methods=['POST'])
def create_user_type():
    if request.method == 'POST':
        try:
            body = request.get_json()
            descr = body.get('descr')
            
            user_type = UserType(descr=descr)
            db.session.add(user_type)
            db.session.commit()
            
            return jsonify({
                'message': "Tipo de usuário criado com sucesso!"
            }), 201
            
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
            
            
@app.route('/api/get_user_types', methods=['GET'])
def get_user_type():
    if request.method == 'GET':
        try:   
            user_types = UserType.query.all()
            schema = UserTypeSchema(many=True)
            payload = schema.dump(user_types)
            return jsonify({
                'users': payload
            }), 200
            
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500


@app.route('/api/authenticate_user', methods=['POST'])
def authenticate_user():
    if request.method == 'POST':
        try:
            body = request.get_json()
            email = body.get('email')
            password = body.get('password')
            
            user = User.query.filter_by(email=email).first()
            
            if user == None:
                return jsonify({
                    'status': 'error',
                    'message': 'user not found!'
                }), 200
                
            checked_password = check_password_hash(user.password_hash, password)
            
            if checked_password: 
                schema = UserSchema()
                payload = schema.dump(user)
                
                return jsonify({
                    'user': payload,
                    'status': 'ok'
                }), 200
            else:
                return jsonify({
                    'status': 'error',
                    'message': 'Senha incorreta!'
                }), 200
                
        except Exception as error:
            print(f'error class: {error.__class__} | error cause: {error.__cause__}')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500