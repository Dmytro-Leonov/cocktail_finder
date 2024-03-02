from sqlalchemy.orm import Mapped, mapped_column


class PrimaryKeyMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
