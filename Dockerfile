FROM python:3.13-slim AS builder

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main.py /code/

CMD ["fastapi","run","main.py","--host=0.0.0.0","--port=8000"]

