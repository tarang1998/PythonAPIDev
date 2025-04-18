"""Changes in the patient and doctor data

Revision ID: 90686fb30dc1
Revises: cf789a09b8fc
Create Date: 2025-03-30 20:43:35.141233

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90686fb30dc1'
down_revision = 'cf789a09b8fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(length=120), nullable=False))
        batch_op.add_column(sa.Column('password', sa.String(length=255), nullable=False))
        batch_op.create_unique_constraint(None, ['email'])

    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password', sa.String(length=255), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('patients', schema=None) as batch_op:
        batch_op.drop_column('password')

    with op.batch_alter_table('doctors', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('password')
        batch_op.drop_column('email')

    # ### end Alembic commands ###
