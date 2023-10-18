"""Correction tablename CharityProject

Revision ID: 02
Revises: 01
Create Date: 2023-10-16 14:44:04.006703

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02'
down_revision = '01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charityproject',
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('close_date', sa.DateTime(), nullable=True),
    sa.Column('full_amount', sa.Integer(), nullable=True),
    sa.Column('invested_amount', sa.Integer(), nullable=True),
    sa.Column('fully_invested', sa.Boolean(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('charityprojrct')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('charityprojrct',
    sa.Column('create_date', sa.DATETIME(), nullable=True),
    sa.Column('close_date', sa.DATETIME(), nullable=True),
    sa.Column('full_amount', sa.INTEGER(), nullable=True),
    sa.Column('invested_amount', sa.INTEGER(), nullable=True),
    sa.Column('fully_invested', sa.BOOLEAN(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    sa.Column('description', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.drop_table('charityproject')
    # ### end Alembic commands ###