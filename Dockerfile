FROM python:3.13

WORKDIR /code

# 保证容器内 Python 能正确解析 routes、models 等包（Railway/uvicorn 加载 app 时 CWD 可能不在 /code）
ENV PYTHONPATH=/code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 复制整个项目代码（main.py 依赖 routes、models、config、core 等模块）
COPY . /code/

# Railway 运行时注入 PORT，本地默认 8080
CMD ["sh", "-c", "fastapi run main.py --host=0.0.0.0 --port=${PORT:-8080}"]
