import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base
from app.db.mixins import PrimaryKeyMixin


class CocktailImage(Base, PrimaryKeyMixin):
    __tablename__ = "cocktail_image"

    cocktail_id: Mapped[int] = mapped_column(sa.ForeignKey("cocktail.id"))
    image: Mapped[str] = mapped_column(sa.String())
    order: Mapped[int] = mapped_column(sa.Integer())
