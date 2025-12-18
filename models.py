from typing import Optional
from sqlmodel import Field, SQLModel


class PostBase(SQLModel):
    title: str
    content: str
    is_published: bool = False

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None,primary_key= True)

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id:int

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None




# ---- 新增UserModel ----

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str



