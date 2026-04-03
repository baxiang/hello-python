"""主应用"""

from fastapi import FastAPI
from .core.database import init_db
from .api import router

app = FastAPI(
    title="股票数据监控系统",
    description="股票行情采集与分析",
    version="0.1.0"
)

app.include_router(router, prefix="/api")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "股票数据监控系统 API", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)