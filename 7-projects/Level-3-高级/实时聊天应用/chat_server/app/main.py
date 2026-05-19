"""主应用"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path

from .api import api_router
from .core import get_settings

settings = get_settings()

app = FastAPI(
    title="实时聊天",
    description="基于 WebSocket 的多人聊天应用",
    version="0.1.0"
)

# 注册路由
app.include_router(api_router)

# 静态文件
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    """聊天页面"""
    index_file = static_dir / "index.html"
    if index_file.exists():
        return index_file.read_text(encoding="utf-8")
    return "<h1>Chat Server</h1><p>请创建 static/index.html</p>"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )