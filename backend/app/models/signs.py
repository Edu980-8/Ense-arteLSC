from typing import TYPE_CHECKING, Optional
import uuid

from sqlmodel import Field, SQLModel, Relationship


if TYPE_CHECKING:
    from app.models.categories import Category
    from app.models.user_signs import UserSign


class SignBase(SQLModel):
    name: str = Field(max_length=255)
    description: str | None = None
    url_video: str

# Properties to return via API, id is always required
class SignPublic(SignBase):
    id: uuid.UUID

class SignsPublic(SQLModel):
    data: list[SignPublic]
    count: int

class Sign(SignBase, table=True):
    __tablename__ = "signs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

category: Optional["Category"] = Relationship(back_populates="signs")
user_signs: list["UserSign"] = Relationship(back_populates="sign")