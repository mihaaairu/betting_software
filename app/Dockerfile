FROM python:3.11-slim as BASE
RUN apt-get update && apt-get install -y curl iputils-ping && apt-get clean
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONIOENCODING=utf-8

FROM base AS DEPENDENCIES
COPY pyproject.toml poetry.lock* /app/
RUN poetry config virtualenvs.create false
WORKDIR app/
RUN poetry install

FROM dependencies AS SOURCES
COPY src/ /app/src
RUN chmod 0744 /app/src/main.py

FROM sources AS FINAL
WORKDIR src/
ENTRYPOINT uvicorn main:app --host 0.0.0.0 --port 8000
