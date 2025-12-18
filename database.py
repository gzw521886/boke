from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

# 初始化数据库表的方法
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


# 依赖项：获取数据库会话
# yield 关键字相当于：
# 1. 打开连接，把 session 给出去
# 2. 等待请求处理完
# 3. 回来执行 finally 里的（如果有）关闭连接逻辑
def get_session():
    with Session(engine) as session:
        yield session

