FROM python:3.13-slim AS builder

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 复制整个项目代码（main.py 依赖 routes、models、config、core 等模块）
COPY . /code/

WORKDIR /code

CMD ["fastapi", "run", "main.py", "--host=0.0.0.0", "--port=8000"]

