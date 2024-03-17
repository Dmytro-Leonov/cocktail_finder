import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.db.mixins import PrimaryKeyMixin


class Tag(Base, PrimaryKeyMixin):
    __tablename__ = "tag"

    name: Mapped[str] = mapped_column(sa.String(50), unique=True)
