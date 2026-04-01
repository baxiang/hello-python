"""主应用"""

from fastapi import FastAPI
from .core import init_db
from .api import router

app = FastAPI(
    title="后台商城系统",
    description="电商后台管理 API",
    version="0.1.0"
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "商城系统 API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)