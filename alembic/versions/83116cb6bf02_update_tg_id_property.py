"""Update tg_id property

Revision ID: 83116cb6bf02
Revises: 454deb3a198c
Create Date: 2025-04-21 10:31:56.139661

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '83116cb6bf02'
down_revision: Union[str, None] = '454deb3a198c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('admins', 'tg_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               nullable=True)
    op.alter_column('users', 'tg_id',
               existing_type=sa.INTEGER(),
               type_=sa.BigInteger(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'tg_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               existing_nullable=True)
    op.alter_column('admins', 'tg_id',
               existing_type=sa.BigInteger(),
               type_=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
