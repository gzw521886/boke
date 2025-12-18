from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import posts, auth # 导入我们的子路由模块

# 初始化 App
app = FastAPI()

# 配置 CORS (和之前一样)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 开发阶段允许所有
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册事件：启动时创建表
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to my Blog API"}