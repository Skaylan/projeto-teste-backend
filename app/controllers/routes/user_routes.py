from app.controllers.utils import print_error_details
from flask import jsonify, request, Blueprint
from app.models.tables.user import User
from app.models.tables.user_type import UserType
from app.models.schemas.user_schema import UserSchema
from app.models.schemas.user_type_schema import UserTypeSchema
from werkzeug.security import generate_password_hash
from app.extensions import db
from sqlalchemy import or_


user_route = Blueprint('user_route', __name__)

@user_route.post('/api/create_user')
def create_user():
    try:
        body = request.get_json()
        name = body.get('name')
        email = body.get('email')
        password = body.get('password')
        user_type_id = body.get('user_type')
        
        password_hash = generate_password_hash(password)
        
        user = User(name=name, email=email, password_hash=password_hash, user_type_id=user_type_id)
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': "Usuario criado com sucesso!"
        }), 201
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500


@user_route.get('/api/get_users')
def get_users():
    try:
        search = request.args.get('search')
        if search == '' or search == 'undefined':
            users = User.query.all()
        elif search != '' or search != 'undefined':
            users = User.query.filter(or_(User.name.like(f'%{search}%'), User.email.like(f'%{search}%'))).all()
            print("aqui>>>", users)
        
        schema = UserSchema(many=True)
        payload = schema.dump(users)
        return jsonify({
            'users': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500


@user_route.get('/api/get_user_by_id')
def get_user_by_id():
    try:
        id = request.args.get('user_id')
        user = User.query.filter_by(id=id).first()
        
        if user == None:
            return jsonify({
                'status': 'error',
                'message': 'Usuario não existe!'
            }), 200
        
        schema = UserSchema()
        payload = schema.dump(user)
        return jsonify({
            'status': 'ok',
            'user': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500

@user_route.post('/api/create_user_type')
def create_user_type():
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
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
            
            
@user_route.get('/api/get_user_types')
def get_user_type():
    try:   
        user_types = UserType.query.all()
        schema = UserTypeSchema(many=True)
        payload = schema.dump(user_types)
        return jsonify({
            'user_types': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500