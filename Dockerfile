FROM python:3.8-alpine
WORKDIR /app
RUN mkdir ~/.heydocker/
COPY ./src/heydocker /app/src/heydocker
COPY pyproject.toml /app/pyproject.toml
RUN python -m pip install -e .