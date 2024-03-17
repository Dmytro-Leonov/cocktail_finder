import sqlalchemy as sa

from app.db import Base

CocktailTag = sa.Table(
    "cocktail_tag",
    Base.metadata,
    sa.Column("cocktail_id", sa.ForeignKey("cocktail.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tag.id"), primary_key=True),
)
