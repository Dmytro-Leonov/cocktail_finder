from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt, StringConstraints

ListOfStrings = list[Annotated[str, StringConstraints(max_length=200)]]


class CocktailCreateIn(BaseModel):
    name: Annotated[str, Field(max_length=200)]
    slug: Annotated[str, StringConstraints(max_length=200)]
    alternative_names: Annotated[ListOfStrings, Field(max_length=5)]
    image: str
    description: Annotated[str, StringConstraints(max_length=2000)]
    sweetness: Annotated[PositiveInt, Field(ge=1, le=10)]
    abv: Annotated[float, Field(ge=0, le=100)]
    calories_per_serving: Annotated[int, Field(ge=0)]
    complexity: Annotated[int, Field(ge=1, le=10)]
    minutes_to_make: Annotated[int, Field(ge=1)]
    # tags: list[int]
    # tags: list[int]
