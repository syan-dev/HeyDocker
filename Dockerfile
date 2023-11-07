FROM python:3.8-slim-buster
WORKDIR /app
RUN apt-get update -y && \
    apt-get install curl -y && \ 
    pip3 install --upgrade pip && \
    mkdir ~/.heydocker/
COPY ./src/heydocker /app/src/heydocker
COPY pyproject.toml /app/pyproject.toml
RUN python -m pip install -e .