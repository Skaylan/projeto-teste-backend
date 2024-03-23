import jwt, os
from app.controllers.utils import print_error_details
from flask import jsonify, request, Blueprint
from app.models.tables.user import User
from app.models.schemas.user_schema import UserSchema
from werkzeug.security import check_password_hash


SECRET_KEY = os.getenv('SECRET_KEY')

auth_route = Blueprint('auth_route', __name__)


@auth_route.post('/api/authenticate_user')
def authenticate_user():
    try:
        body = request.get_json()
        email = body.get('email')
        password = body.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user == None:
            return jsonify({
                'status': 'error',
                'message': 'Usuario não existe!'
            }), 200
            
        checked_password = check_password_hash(user.password_hash, password)
        
        if checked_password: 
            schema = UserSchema()
            payload = schema.dump(user)
            token = jwt.encode({"email": user.email, 'id': user.id, 'name': user.name}, SECRET_KEY)
            
            return jsonify({
                'token': token, 
                'user': payload,
                'status': 'ok'
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Senha incorreta!'
            }), 200
            
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500