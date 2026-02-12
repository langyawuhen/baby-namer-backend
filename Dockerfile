# 构建阶段
FROM python:3.13-slim AS builder

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user

# 运行阶段
FROM python:3.13-slim

WORKDIR /code
COPY --from=builder /root/.local /root/.local

# 显式复制应用代码，避免漏拷或 .dockerignore 误伤
COPY main.py dependence.py ./
COPY config/ core/ models/ repository/ routes/ schemas/ ./
COPY alembic/ alembic.ini ./

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/code

EXPOSE 8080
# 在启动命令里再次设置 PYTHONPATH，防止被部署平台覆盖
CMD ["/bin/sh", "-c", "PYTHONPATH=/code exec uvicorn main:app --host 0.0.0.0 --port 8080"]
