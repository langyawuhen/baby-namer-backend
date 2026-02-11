# 构建阶段
FROM python:3.13-slim AS builder

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user

# 运行阶段
FROM python:3.13-slim

WORKDIR /code
COPY --from=builder /root/.local /root/.local
# 复制应用代码（根目录 main.py + 各模块）
COPY main.py dependence.py ./
COPY config/ core/ models/ repository/ routes/ schemas/ ./
COPY alembic/ alembic.ini ./

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
