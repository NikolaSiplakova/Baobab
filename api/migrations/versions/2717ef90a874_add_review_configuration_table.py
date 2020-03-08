"""empty message

Revision ID: 2717ef90a874
Revises: 02242641e122
Create Date: 2020-02-29 09:23:29.153652

"""

# revision identifiers, used by Alembic.
revision = '2717ef90a874'
down_revision = '02242641e122'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('review_configuration',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('review_form_id', sa.Integer(), nullable=False),
    sa.Column('num_reviews_required', sa.Integer(), nullable=False),
    sa.Column('num_optional_reviews', sa.Integer(), nullable=False),
    sa.Column('drop_optional_question_id', sa.Integer(), nullable=True),
    sa.Column('drop_optional_agreement_values', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['drop_optional_question_id'], ['review_question.id'], ),
    sa.ForeignKeyConstraint(['review_form_id'], ['review_form.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review_configuration')
    # ### end Alembic commands ###
