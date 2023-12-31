"""empty message

Revision ID: 5ce26414573b
Revises: 32dc5c70ede5
Create Date: 2023-07-20 22:26:23.568763

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision = '5ce26414573b'
down_revision = '32dc5c70ede5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Items', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(), nullable=True))
        batch_op.alter_column('price',
               existing_type=mssql.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Items', schema=None) as batch_op:
        batch_op.alter_column('price',
               existing_type=sa.Float(precision=2),
               type_=mssql.REAL(),
               existing_nullable=False)
        batch_op.drop_column('description')

    # ### end Alembic commands ###
