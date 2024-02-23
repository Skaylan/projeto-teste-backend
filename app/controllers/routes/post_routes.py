from app.controllers.utils import print_error_details
from flask import jsonify, request, Blueprint
from app.models.tables.user import User
from app.models.tables.post import Post
from app.models.tables.reply import Reply
from app.models.tables.comment import Comment
from app.models.schemas.post_schema import PostSchema
from app.models.schemas.reply_schema import ReplySchema
from app.models.schemas.comments_schema import CommentSchema
from app.extensions import db


post_route = Blueprint('post_route', __name__)

@post_route.post('/api/create_post')
def create_post():
    try:
        body = request.get_json()
        content = body.get('content')
        owner_id = body.get('owner_id')
        user = User.query.filter_by(id=owner_id).first()
        post = Post(content=content, owner_id=user.id)
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
            
            
@post_route.get('/api/generate_feed')
def generate_feed():
    try:
        id = request.args.get('user_id')
        
        posts = Post.query.order_by(Post.created_at.desc()).all()
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

   
@post_route.get('/api/get_posts')
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


@post_route.delete('/api/delete_post')
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
      
        
@post_route.post('/api/comment_on_post')
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
        
        
@post_route.get('/api/get_post_comments')
def get_post_comments():
    try:
        PER_PAGE = 3
        post_id = request.args.get('post_id')
        page = request.args.get('page', 1, type=int)
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
   
        
@post_route.post('/api/reply_comment')
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
        
        
@post_route.get('/api/get_comment_replies')
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