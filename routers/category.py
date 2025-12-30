from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from database import get_session
from jose import jwt, JWTError
from models import Category, CategoryCreate, CategoryRead, User
from typing import List, Optional
from security import SECRET_KEY, ALGORITHM        # 导入刚才写的模型



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

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

@router.post("/categories/",response_model=CategoryRead, tags=["categories"])
def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.get("/categories/",response_model=List[CategoryRead], tags=["categories"])
def read_categories(session: Session = Depends(get_session)):
    categories = session.exec(select(Category)).all()
    return categories

