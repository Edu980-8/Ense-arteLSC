from typing import TYPE_CHECKING, Optional
import uuid
from sqlmodel import Field, SQLModel, Relationship



if TYPE_CHECKING:
    from app.models.signs import Sign
    from app.models.users import User


class UserSignBase(SQLModel):
    position: int


class UserSign(UserSignBase, table=True):
    __tablename__ = "user_signs"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    sign_id: uuid.UUID = Field(foreign_key="signs.id")
    user_id: uuid.UUID = Field(foreign_key="users.id")
    sign: Optional["Sign"] = Relationship(back_populates="user_signs")
    user: Optional["User"] = Relationship(back_populates="user_signs")
