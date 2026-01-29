FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock .

RUN uv sync --locked --no-dev

COPY crd ./crd

ENTRYPOINT ["uv", "run", "-m", "crd.main"]