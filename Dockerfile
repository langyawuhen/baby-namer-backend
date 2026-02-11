# 构建阶段
FROM python:3.13-slim as builder

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt --user

# 运行阶段
FROM python:3.13-slim

WORKDIR /code
COPY --from=builder /root/.local /root/.local
COPY ./src /code/src

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
