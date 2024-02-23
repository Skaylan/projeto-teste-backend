from app.extensions import db
from app.models.tables.company import Company
from flask import jsonify, request, Blueprint
from app.models.tables.user_company import UserCompany
from app.controllers.utils import print_error_details


company_route = Blueprint('company_route', __name__)


@company_route.post('/api/create_company')
def create_company():
    try:
        body = request.get_json()

        company = Company(
            cnpj=body.get('cnpj'), 
            company_name=body.get('company_name'), 
            trading_name=body.get('trading_name'), 
            address=body.get('address'), 
            city=body.get('city'), 
            state=body.get('state'), 
            phone=body.get('phone')
        )
        user_company = UserCompany(company_id=company.id, user_id=body.get('user_id'))
        
        db.session.add(company)
        db.session.add(user_company)
        db.session.commit()

        return jsonify({
            'status': 'ok',
          	'message': 'Company created successfully!'
        }), 201
        
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
          'status': 'error',
          'message': 'An error has occurred!',
          'error_class': str(error.__class__),
          'error_cause': str(error.__cause__)
        }), 500