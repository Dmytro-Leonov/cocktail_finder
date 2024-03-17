import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base
from app.db.mixins import CreatedUpdatedMixin, PrimaryKeyMixin

from .cocktail_image import CocktailImage
from .cocktail_tag import CocktailTag
from .tag import Tag


class Cocktail(Base, PrimaryKeyMixin, CreatedUpdatedMixin):
    __tablename__ = "cocktail"

    slug: Mapped[str] = mapped_column(sa.String(200), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(sa.String(200), unique=True, nullable=False)
    alternative_names: Mapped[list[str]] = mapped_column(
        sa.ARRAY(sa.String(200), dimensions=1), default=[], nullable=False
    )
    image: Mapped[str] = mapped_column(sa.String(), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text(), nullable=False)

    # 1-10
    sweetness: Mapped[int] = mapped_column(sa.Integer(), index=True, nullable=False)

    # Alcohol by volume (0-100)%
    abv: Mapped[float] = mapped_column(sa.Float(), index=True, nullable=False)

    calories_per_serving: Mapped[int] = mapped_column(
        sa.Integer(), index=True, nullable=False
    )

    # 0-10
    rating: Mapped[float] = mapped_column(
        sa.Float(),
        default=0,
        index=True,
        nullable=False,
    )

    # 1-10
    complexity = mapped_column(sa.Integer(), nullable=False)
    minutes_to_make = mapped_column(sa.Integer(), nullable=False)

    images: Mapped[list[CocktailImage]] = relationship("CocktailImage")
    tags: Mapped[list[Tag]] = relationship("Tag", secondary=CocktailTag)
