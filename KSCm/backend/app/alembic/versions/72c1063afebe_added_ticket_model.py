"""added ticket model

Revision ID: 72c1063afebe
Revises: 17577b966ca2
Create Date: 2021-02-09 15:55:34.413056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '72c1063afebe'
down_revision = '17577b966ca2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ticket',
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ticket_id', sa.Integer(), nullable=True),
    sa.Column('contract_nr', sa.Integer(), nullable=True),
    sa.Column('customer_name', sa.String(), nullable=True),
    sa.Column('status', sa.Enum('NEW', 'OPEN_QUESTION', 'ANSWERED_QUESTION', 'IN_PROGRESS', 'ORDERED', 'CLOSED', name='ticketstatus'), nullable=True),
    sa.Column('kind', sa.Enum('IMPORTED', 'COMMISSION', 'CLAIM', 'CONNECTED', 'INCOMPLETE', name='ticketkind'), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('store_internal_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['store_internal_id'], ['store.internal_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ticket_contract_nr'), 'ticket', ['contract_nr'], unique=False)
    op.create_index(op.f('ix_ticket_customer_name'), 'ticket', ['customer_name'], unique=False)
    op.create_index(op.f('ix_ticket_id'), 'ticket', ['id'], unique=False)
    op.create_index(op.f('ix_ticket_ticket_id'), 'ticket', ['ticket_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ticket_ticket_id'), table_name='ticket')
    op.drop_index(op.f('ix_ticket_id'), table_name='ticket')
    op.drop_index(op.f('ix_ticket_customer_name'), table_name='ticket')
    op.drop_index(op.f('ix_ticket_contract_nr'), table_name='ticket')
    op.drop_table('ticket')
    # ### end Alembic commands ###
