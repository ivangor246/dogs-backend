FROM python:3.13.2

RUN apt-get update \
    && apt-get install -y netcat-traditional

WORKDIR /app

COPY requirements.txt .

ARG HTTP_PROXY
ARG HTTPS_PROXY

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT ["sh", "entrypoint.sh"]
