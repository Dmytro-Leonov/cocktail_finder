from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

from app.db.constants import DB_NAMING_CONVENTION

metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)

Base = declarative_base(metadata=metadata)
