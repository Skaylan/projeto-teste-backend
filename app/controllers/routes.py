import os
import sys
from app import app
from app.controllers.utils import print_error_details
from flask import jsonify, request
from app.config.db_config import *
from app.config.app_config import *
from app.models.tables.user import User
from app.models.tables.post import Post
from app.models.tables.reply import Reply
from app.models.tables.comment import Comment
from app.models.tables.user_type import UserType
from app.models.schemas.user_schema import UserSchema
from app.models.schemas.post_schema import PostSchema
from app.models.schemas.reply_schema import ReplySchema
from app.models.schemas.comments_schema import CommentSchema
from app.models.schemas.user_type_schema import UserTypeSchema
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

SECRET_KEY = os.getenv('SECRET_KEY')

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
            print_error_details(error)
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
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500


@app.route('/api/get_user_by_id', methods=['GET'])
def get_user_by_id():
    if request.method == 'GET':
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
            print_error_details(error)
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
            print_error_details(error)
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
                    'message': 'Usuario não existe!'
                }), 200
                
            checked_password = check_password_hash(user.password_hash, password)
            
            if checked_password: 
                schema = UserSchema()
                payload = schema.dump(user)
                token = jwt.encode({"email": user.email, 'id': user.id}, SECRET_KEY)
                
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
            
@app.route('/api/create_post', methods=['POST'])
def create_post():
    if request.method == 'POST':
        try:
            body = request.get_json()
            content = body.get('content')
            owner_id = body.get('owner_id')
            user = User.query.filter_by(id=owner_id).first()
            post = Post(content=content, owner=user.id)
            db.session.add(post)
            db.session.commit()
            
            return jsonify({
                'status': 'ok',
                'message': 'Post criado com sucesso!'
            }), 201
            
        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500
            
            
@app.route('/api/generate_feed', methods=['GET'])
def generate_feed():
    if request.method == 'GET':
        try:
            id = request.args.get('user_id')
            
            posts = Post.query.filter_by(owner=id).order_by(Post.created_at.desc()).all()
            schema = PostSchema(many=True)
            payload = schema.dump(posts)
            
            return jsonify({
                'status': 'ok',
                'posts': payload
            }), 201
            
        except Exception as error:
            print_error_details(error)
            return jsonify({
                    'status': 'error',
                    'message': 'An error has occurred!',
                    'error_class': str(error.__class__),
                    'error_cause': str(error.__cause__)
                }), 500

   
@app.get('/api/get_posts')
def get_posts():
    try:
        posts = Post.query.all()
        schema = PostSchema(many=True)
        payload = schema.dump(posts)
        
        return jsonify({
            'status': 'ok',
            'posts': payload
        }), 201
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500


@app.delete('/api/delete_post')
def delete_post():
    try:
        body = request.get_json()
        post_id = body.get('post_id')
        Reply.query.filter_by(post_id=post_id).delete()
        Comment.query.filter_by(post_id=post_id).delete()
        post = Post.query.filter_by(id=post_id).first()
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({
            'status': 'ok',
            'message': 'post deletado com sucesso!'
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
      
        
@app.post('/api/comment_on_post')
def comment_on_post():
    try:
        body = request.get_json()
        post_id = body.get('post_id')
        content = body.get('comment')
        owner_id = body.get('owner_id')
        
        comment = Comment(comment=content, post_id=post_id, owner_id=owner_id)
        db.session.add(comment)
        db.session.commit()
        
        schema = CommentSchema()
        payload = schema.dump(comment)
        
        return jsonify({
            'status': 'ok',
            'message': 'commentario adicionado com sucesso!',
            'comment': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
        
        
@app.get('/api/get_post_comments')
def get_post_comments():
    try:
        PER_PAGE = 3
        post_id = request.args.get('post_id')
        page = request.args.get('page', 1, type=int)
        print(page)
        comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc())
        comments = comments.paginate(page=page, per_page=PER_PAGE, error_out=False)
        schema = CommentSchema(many=True)
        payload = schema.dump(comments.items)
        
        return jsonify({
            'status': 'ok',
            'comments': payload,
        }), 200
        
            
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
   
        
@app.post('/api/reply_comment')
def reply_comment():
    try:
        body = request.get_json()
        reply_message = body.get('reply_message')
        comment_id = body.get('comment_id')
        owner_id = body.get('owner_id')
        post_id = body.get('post_id')
        
        reply = Reply(comment=reply_message, owner_id=owner_id, parent_comment_id=comment_id, post_id=post_id)
        db.session.add(reply)
        db.session.commit()
        
        schema = CommentSchema()
        payload = schema.dump(reply)
        
        return jsonify({
            'status': 'ok',
            'message': 'resposta adicionada com sucesso!',
            'reply': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
        
        
@app.get('/api/get_comment_replies')
def get_comment_replies():
    try:
        comment_id = request.args.get('comment_id')
        
        replies = Reply.query.filter_by(parent_comment_id=comment_id).order_by(Reply.created_at.desc()).all()
        schema = ReplySchema(many=True)
        payload = schema.dump(replies)
        
        return jsonify({
            'status': 'ok',
            'replies': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500