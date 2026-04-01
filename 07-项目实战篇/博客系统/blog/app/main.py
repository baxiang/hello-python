"""主应用"""

from fastapi import FastAPI
from .core import init_db
from .api import router

app = FastAPI(
    title="博客系统",
    description="基于 FastAPI 的 RESTful API",
    version="0.1.0"
)

# 注册路由
app.include_router(router, prefix="/api")

# 初始化数据库
@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "博客系统 API", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)