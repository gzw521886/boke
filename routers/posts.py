from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlmodel import Session, select
from database import get_session  # 导入刚才写的数据库依赖
from models import Post, PostCreate, PostRead, PostUpdate, User 
from security import SECRET_KEY, ALGORITHM        # 导入刚才写的模型



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# 创建一个路由实例
router = APIRouter()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:

    # 验证 JWT token 并返回当前用户
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.username == username)).first()

    if user is None:
        raise credentials_exception
    return user
        

@router.post("/", response_model= PostRead)
def create_post(post: PostCreate, session: Session = Depends(get_session),current_user:User = Depends(get_current_user)):

    db_post = Post.model_validate(post)

    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post

@router.get("/", response_model = List[PostRead])
def read_posts(session: Session = Depends(get_session)):
    posts = session.exec(select(Post)).all()
    return posts


@router.get("/{post_id}", response_model=PostRead)
def read_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/{post_id}",response_model=PostRead)
def update_post(post_id: int, post_data: PostUpdate, session: Session = Depends(get_session),current_user:User = Depends(get_current_user)):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    update_data = post_data.model_dump(exclude_unset=True)

    db_post.sqlmodel_update(update_data)

    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.delete("/{post_id}")
def delete_post(post_id: int, session: Session = Depends(get_session),current_user:User = Depends(get_current_user)):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    session.delete(db_post)
    session.commit()
    return {"ok": True}