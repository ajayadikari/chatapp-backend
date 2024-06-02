FROM python:3.11-slim

WORKDIR /chatapp

COPY requirements.txt /chatapp/

COPY . /chatapp/

RUN apt-get update \
    && apt-get install -y python3-pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python3 manage.py makemigrations \
    && python3 manage.py migrate

EXPOSE 8000

CMD ["uvicorn", "chatappbase.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
