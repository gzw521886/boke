from typing import List
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel, table


class CategoryBase(SQLModel):
    name: str = Field(index=True, unique=True)

class Category(CategoryBase,table=True):
    id: Optional[int] = Field(default=None,primary_key=True)
    posts:List["Post"] = Relationship(back_populates="category")

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int


class PostBase(SQLModel):
    title: str
    content: str
    is_published: bool = False
    # 新增字段 摘要和封面
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")

class Post(PostBase, table=True):
    id: Optional[int] = Field(default=None,primary_key= True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    category: Optional[Category] = Relationship(back_populates="posts")

class PostCreate(PostBase):
    pass

class PostRead(PostBase):
    id:int
    created_at: datetime
    updated_at: datetime

class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None
    summary: Optional[str] = None
    cover_image: Optional[str] = None
    category_id: Optional[int] = None








# ---- 新增UserModel ----

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    avatar: Optional[str] = None
    nickname: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str



