import sys
from pathlib import Path

# 将 main.py 所在目录（项目根）加入 Python 路径，避免 Railway/Docker 等环境下找不到 routes
_root = Path(__file__).resolve().parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from fastapi import FastAPI
from routes.user import router as user_router
from routes.article import router as article_router
from routes.agent import router as agent_router
from fastapi.middleware.cors import CORSMiddleware
import models

app = FastAPI()

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有域名，生产环境需指定具体域名（如"http://localhost:8080"）
    allow_credentials=True,  # 允许携带 Cookie
    allow_methods=["*"],  # 允许所有请求方法（GET/POST/PUT/DELETE 等）
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(user_router, prefix="/api")
app.include_router(article_router, prefix="/api")
app.include_router(agent_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Hello World"}


# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=8080)