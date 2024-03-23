from app.controllers.utils import print_error_details
from flask import jsonify, request, Blueprint
from app.models.tables.friendship import Friendship
from app.models.schemas.friendship_schema import FriendshipSchema
from app.extensions import db


friend_route = Blueprint('friend_route', __name__)

@friend_route.post('/api/add_friend')
def add_friend():
  try:
    body = request.get_json()
    user_id = body.get('user_id')
    friend_id = body.get('friend_id')

    friend1 = Friendship(user_id=user_id, friend_id=friend_id)
    friend2 = Friendship(user_id=friend_id, friend_id=user_id)
    db.session.add(friend1)
    db.session.add(friend2)
    db.session.commit()

    return jsonify({
      'status': 'ok',
      'message': 'Friend added successfully!'
    }), 201

  except Exception as error:
    print_error_details(error)
    return jsonify({
      'status': 'error',
      'message': 'An error has occurred!',
      'error_class': str(error.__class__),
      'error_cause': str(error.__cause__)
    }), 500


@friend_route.get('/api/get_user_friends')
def get_user_friends():
    try:
        user_id = request.args.get('user_id')
        friends = Friendship.query.filter_by(user_id=user_id).all()
        schema = FriendshipSchema(many=True)
        payload = schema.dump(friends)
        
        return jsonify({
          'status': 'ok',
          'friends': payload
        })
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
          'status': 'error',
          'message': 'An error has occurred!',
          'error_class': str(error.__class__),
          'error_cause': str(error.__cause__)
        }), 500