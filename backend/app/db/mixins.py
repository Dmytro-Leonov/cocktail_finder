from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column


class PrimaryKeyMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class CreatedUpdatedMixin:
    created_at: Mapped[str] = mapped_column(
        sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
    )
    updated_at: Mapped[Optional[str]] = mapped_column(
        sa.DateTime(timezone=True), onupdate=sa.func.now()
    )
