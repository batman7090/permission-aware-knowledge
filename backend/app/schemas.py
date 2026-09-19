
from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: str
    department: str


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DocumentBase(BaseModel):
    title: str
    source: str | None = None
    department: str | None = None
    classification: str


class DocumentCreate(DocumentBase):
    pass


class DocumentRead(DocumentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)