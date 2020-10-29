"""Add Tag models

Revision ID: d7dfd413e768
Revises: 33b563f7be6b
Create Date: 2020-10-24 21:35:38.934050

"""

# revision identifiers, used by Alembic.
revision = 'd7dfd413e768'
down_revision = '33b563f7be6b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['event_id'], ['event.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag_translation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('language', sa.String(length=2), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('tag_id', 'language', name='uq_tag_id_language')
    )
    op.create_table('response_tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('response_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['response_id'], ['response.id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('response_tag')
    op.drop_table('tag_translation')
    op.drop_table('tag')
    # ### end Alembic commands ###
