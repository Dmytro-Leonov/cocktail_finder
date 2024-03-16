import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.db.mixins import PrimaryKeyMixin


class User(Base, PrimaryKeyMixin):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(sa.String(32), unique=True)
    email: Mapped[str] = mapped_column(sa.String(50), unique=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
