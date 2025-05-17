from typing import TYPE_CHECKING
import uuid

from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .user_signs import Sign
    from .medals import Medal

class CategoryBase(SQLModel):
    value: str = Field(index=True, sa_column_kwargs={"unique": True})
    medal_image_url: str = None

class Category(CategoryBase, table=True):
    __tablename__ = "categories"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    signs: list["Sign"] = Relationship(back_populates="category")
    medals: list["Medal"] = Relationship(back_populates="category")