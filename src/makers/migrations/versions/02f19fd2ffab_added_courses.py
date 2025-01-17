"""added_courses

Revision ID: 02f19fd2ffab
Revises: dbdc49011c80
Create Date: 2024-03-16 05:06:12.116390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02f19fd2ffab'
down_revision = 'dbdc49011c80'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('user_id', sa.BigInteger(), nullable=True),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('duration', sa.SMALLINT(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('price', sa.SMALLINT(), nullable=True),
    sa.Column('is_active', sa.BOOLEAN(), nullable=True),
    sa.Column('is_deactivated', sa.BOOLEAN(), nullable=True),
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['mentors.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_created_at'), 'courses', ['created_at'], unique=False)
    op.create_index(op.f('ix_courses_id'), 'courses', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_courses_id'), table_name='courses')
    op.drop_index(op.f('ix_courses_created_at'), table_name='courses')
    op.drop_table('courses')
    # ### end Alembic commands ###
