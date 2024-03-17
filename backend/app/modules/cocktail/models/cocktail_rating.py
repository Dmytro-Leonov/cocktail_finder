import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class CocktailRating(Base):
    __tablename__ = "cocktail_rating"

    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), primary_key=True)
    cocktail_id: Mapped[int] = mapped_column(
        sa.ForeignKey("cocktail.id"), primary_key=True
    )
    rating: Mapped[float] = mapped_column(sa.Integer())  # 1-10
