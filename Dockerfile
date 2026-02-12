# 构建阶段
FROM python:3.13-slim AS builder

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --user

# 运行阶段
FROM python:3.13-slim

WORKDIR /code
COPY --from=builder /root/.local /root/.local
# 复制应用代码（.dockerignore 已排除无关文件）
COPY . .

ENV PATH=/root/.local/bin:$PATH
# 让 Python 能正确解析 routes、config、core 等包（必须）
ENV PYTHONPATH=/code

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
