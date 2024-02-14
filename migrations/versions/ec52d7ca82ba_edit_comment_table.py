"""edit comment table

Revision ID: ec52d7ca82ba
Revises: 7af64dc2a4ec
Create Date: 2024-02-12 23:11:37.227779

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec52d7ca82ba'
down_revision = '7af64dc2a4ec'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint('comment_ibfk_3', type_='foreignkey')
        batch_op.create_foreign_key(None, 'comment', ['reply_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('comment_ibfk_3', 'post', ['reply_id'], ['id'])

    # ### end Alembic commands ###