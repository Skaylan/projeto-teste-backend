from app.controllers.utils import print_error_details
from flask import jsonify, request, Blueprint
from app.models.tables.user import User
from app.models.tables.post_images import PostImages
from app.models.tables.group_custom_theme import GroupCustomTheme
from app.models.tables.group import Group
from app.models.tables.user_group import UserGroup
from app.models.tables.post import Post
from app.models.tables.reply import Reply
from app.models.tables.comment import Comment
from app.models.tables.friendship import Friendship
from app.models.schemas.post_schema import PostSchema
from app.models.schemas.reply_schema import ReplySchema
from app.models.schemas.comments_schema import CommentSchema
from app.extensions import db
from sqlalchemy import or_
from uuid import uuid4
from app.controllers.utils import convert_base64_to_image, compress_image, convert_image_to_base64

IMAGES_SAVE_PATH = 'C://Users//lucas//Documents//projetos//projeto-teste//backend//app//images'


social_media_route = Blueprint('social_media_route', __name__)

@social_media_route.post('/api/create_post')
def create_post():
    try:
        body = request.get_json()
        image_base64_string = body.get('image')
        file_name = str(uuid4())
        content = body.get('content')
        owner_id = body.get('owner_id')
        user = User.query.filter_by(id=owner_id).first()
        has_image = body.get('has_image')
        
        if has_image:
            post = Post(content=content, owner_id=user.id, has_image=True)
            db.session.add(post)
            db.session.commit()

            post_image = PostImages(image_uuid=file_name, post_id=post.id)
            db.session.add(post_image)
            db.session.commit()
            
            convert_base64_to_image(image_base64_string, image_uuid=file_name, save_path=IMAGES_SAVE_PATH)
            compress_image(file_name, IMAGES_SAVE_PATH)
        else:
            post = Post(content=content, owner_id=user.id, has_image=False)
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
            
            
@social_media_route.get('/api/generate_feed')
def generate_feed():
    try:
        id = request.args.get('user_id')
        friendships = Friendship.query.filter_by(user_id=id).all()
        ids = [friend.friend_id for friend in friendships]
        ids.append(id)
        
        posts = Post.query.filter(Post.owner_id.in_(ids)).order_by(Post.created_at.desc()).all()
        
        posts_ids = [post.id for post in posts]
        

        schema = PostSchema(many=True)
        payload = schema.dump(posts)
        for i, _ in enumerate(payload):
            # print("AQUI >>>>>", payload[i])
            if payload[i]['has_image']:
                post_id = payload[i]['id']
                post_image = PostImages.query.filter_by(post_id=post_id).first()
                payload[i]['image'] = convert_image_to_base64(IMAGES_SAVE_PATH, post_image.image_uuid)
            
        for i, _ in enumerate(payload):
            posts_comments = Comment.query.filter_by(post_id=payload[i]['id']).count()
            payload[i]['commentsAmout'] = posts_comments
            

        
        return jsonify({
            'status': 'ok',
            'posts': payload
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500

   
@social_media_route.get('/api/get_posts')
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


@social_media_route.delete('/api/delete_post')
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
      
        
@social_media_route.post('/api/comment_on_post')
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
        
        
@social_media_route.get('/api/get_post_comments')
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
   
        
@social_media_route.post('/api/reply_comment')
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
        
        
@social_media_route.get('/api/get_comment_replies')
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
        

@social_media_route.post('/api/create_group')
def create_group():
    try:
        body = request.get_json()
        group_name = body.get('group_name')
        group_description = body.get('group_description')
        user_id = body.get('user_id')
        tags = body.get('tags')
        image_base64 = body.get('image_base64')
        
        
        return jsonify({
            'data': {'group_name': group_name, 
                    'group_description': group_description, 
                    'user_id': user_id, 
                    'tags': tags, 
                    'image_base64': image_base64
                    },
            'status': 'ok',
            'message': 'ok'    
        }), 200
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500