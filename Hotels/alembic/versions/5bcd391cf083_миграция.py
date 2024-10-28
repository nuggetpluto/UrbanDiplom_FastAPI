"""миграция

Revision ID: 5bcd391cf083
Revises: 863ff3e63000
Create Date: 2024-10-28 16:42:21.719142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '5bcd391cf083'
down_revision: Union[str, None] = '863ff3e63000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создание таблицы customer
    op.create_table(
        'customer',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('second_name', sa.String, nullable=False),
        sa.Column('phone', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('address', sa.String, nullable=False),
    )

    # Создание таблицы hotel
    op.create_table(
        'hotel',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
    )


def downgrade() -> None:
    # Удаление таблицы hotel
    op.drop_table('hotel')

    # Удаление таблицы customer
    op.drop_table('customer')
