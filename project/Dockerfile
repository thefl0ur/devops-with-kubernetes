FROM ghcr.io/astral-sh/uv:python3.13-alpine

ARG PORT=8000

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN uv sync --locked

ADD ./todo_app/ .

EXPOSE ${PORT}

ENV PORT=${PORT}

CMD ["uv", "run", "main.py"]