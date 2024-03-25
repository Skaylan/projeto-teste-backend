from app.controllers.utils import print_error_details
from flask import jsonify, Blueprint
from app.models.tables.post import Post
from app.models.tables.reply import Reply
from app.models.tables.comment import Comment
from sqlalchemy import text
from datetime import datetime
from sqlalchemy.orm import aliased
from app.extensions import db
from app.models.tables.area import Area
from app.models.tables.company import Company
from app.models.tables.theme import Theme
from app.models.tables.form_diagnostic import FormDiagnostic
from app.models.tables.form_theme_response import FormThemeResponse
from app.models.tables.user_company import UserCompany
from app.models.tables.skill import Skill
from app.models.tables.form_skill_response import FormSkillResponse
from app.models.tables.question import Question
from app.models.tables.form_question_response import FormQuestionResponse
from app.models.tables.form_theme_response import FormThemeResponse
from app.controllers.utils import convert_image_to_base64
from app.controllers.routes.social_media_routes import IMAGES_SAVE_PATH

route_for_testing = Blueprint('route_for_testing', __name__)

@route_for_testing.get('/api/test_view')
def test_view():
    try:
        
        # start = datetime.now()
        result = db.session.execute(text("SELECT * FROM feedview"))
        payload = {"posts": []}
        current_post = None
        current_comment = None

        # Itera sobre os resultados da consulta
        for r in result:
            # Se o post atual é diferente do post anterior, cria um novo objeto post
            if current_post is None or current_post["post_id"] != r.post_id:
                current_post = {
                    "post_id": r.post_id,
                    "post_content": r.content,
                    "post_owner_id": r.post_owner_id,
                    "user_id": r.user_id,  # Adiciona a informação do usuário do post
                    "user_full_name": r.user_name, # Adiciona a informação do nome do usuário do post
                    "created_at": r.created_at,
                    "comments": []
                }
                payload["posts"].append(current_post)

            # Se o comentário atual é diferente do comentário anterior, cria um novo objeto comentário
            if current_comment is None or current_comment["comment_id"] != r.comment_id:
                current_comment = {
                    "comment_id": r.comment_id,
                    "comment_content": r.comment,
                    "comment_owner_id": r.comment_owner_id,
                    "user_id": r.user_id,  # Adiciona a informação do usuário do comentário
                    "user_full_name": r.user_name,  # Adiciona a informação do nome do usuário do comentário
                    "replies": []
                }
                current_post["comments"].append(current_comment)

            # Adiciona as respostas ao objeto de comentário
            current_comment["replies"].append({
                "reply_id": r.reply_id,
                "reply_content": r.content_reply,
                "reply_owner_id": r.reply_owner_id,
                "user_id": r.user_id,  # Adiciona a informação do usuário da resposta
            })
        
        end = datetime.now()
        
        return jsonify({
            'status': 'ok',
            'message': 'ok',
            'payload': payload,
        }), 200
        
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500
        
        
@route_for_testing.get('/api/test_sqlalchemy')
def test_sqlalchemy():
    try:
        
        # start = datetime.now()
        PostAlias = aliased(Post)
        CommentAlias = aliased(Comment)
        ReplyAlias = aliased(Reply)

        result = db.session.query(
            PostAlias.id.label('post_id'),
            PostAlias.content,
            PostAlias.owner.label('post_owner_id'),
            CommentAlias.id.label('comment_id'),
            CommentAlias.comment,
            CommentAlias.owner_id.label('comment_owner_id'),
            ReplyAlias.id.label('reply_id'),
            ReplyAlias.comment.label('content_reply'),
            ReplyAlias.owner_id.label('reply_owner_id')
        ).outerjoin(CommentAlias, PostAlias.id == CommentAlias.post_id)\
        .outerjoin(ReplyAlias, CommentAlias.id == ReplyAlias.parent_comment_id)\
        .limit(100).all()
        
        print(result)
        
        payload = [{
                "post_id": r.post_id,
                "post_content": r.content,
                "post_owner_id": r.post_owner_id,
                "comment_id": r.comment_id,
                "comment_content": r.comment,
                "comment_owner_id": r.comment_owner_id,
                "reply_id": r.reply_id,
                "reply_content": r.content_reply,
                "reply_owner_id": r.reply_owner_id
            } for r in result]
        # end = datetime.now()
        
        return jsonify({
            'status': 'ok',
            'message': 'ok',
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
        
        
@route_for_testing.get('/api/get_img')
def get_img():
    try:
        image = convert_image_to_base64(IMAGES_SAVE_PATH, '1')
        return jsonify({
            'status': 'ok',
            'message': 'ok',
            'image': image
        })
    except Exception as error:
        print_error_details(error)
        return jsonify({
                'status': 'error',
                'message': 'An error has occurred!',
                'error_class': str(error.__class__),
                'error_cause': str(error.__cause__)
            }), 500