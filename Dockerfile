FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run marimo run --no-skew-protection --no-token src/plot_stress_2d/app.py --host 0.0.0.0 --port ${PORT}"]