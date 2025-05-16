from typing import TYPE_CHECKING, Optional
import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint

if TYPE_CHECKING:
    from app.models.users import User
    from app.models.categories import Category
    
class MedalBase(SQLModel):
    certificate_type: str = Field(default="Completed")
    issuance_date: datetime = Field(default_factory=datetime.utcnow)

class MedalCreate(MedalBase):
    category_id: uuid.UUID
    user_id: uuid.UUID

# Properties to return via API, id is always required
class MedalPublic(MedalBase):
    id: uuid.UUID
    category_id: uuid.UUID
    user_id: uuid.UUID

class MedalsPublic(SQLModel):
    data: list[MedalPublic]
    count: int

class Medal(MedalBase, table=True):
    __tablename__ = "medals"
    __table_args__ = (
        UniqueConstraint("category_id", "user_id", name="uix_category_user"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category_id: uuid.UUID = Field(foreign_key="categories.id")
    user_id: uuid.UUID = Field(foreign_key="users.id", index=True)

user: Optional["User"] = Relationship(back_populates="medals")
category: Optional["Category"] = Relationship(back_populates="medals")