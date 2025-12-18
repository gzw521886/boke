from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
from jose import jwt

# 1. 配置参数
# 在真实项目中，SECRET_KEY 应该是一个很长很复杂的随机字符串，并且放在环境变量里
SECRET_KEY = "my_super_secret_key_change_this" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 2. 密码加密工具
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """验证明文密码和数据库里的哈希密码是否匹配"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    """把明文密码加密成哈希值"""
    return pwd_context.hash(password)

# 3. Token 生成工具
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # 设置过期时间
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt