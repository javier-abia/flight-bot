# Install uv
FROM python:3.12-slim

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:0.5.7 /uv /bin/

# Set working directory
WORKDIR /app

# Set environment variables
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    libssl-dev \
    libffi-dev \
    python3-dev \
    gcc \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Install project dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy project files
COPY . /app

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Set PATH for virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Create non-root user
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app

# Add webdriver path to environment
ENV PATH="/usr/lib/chromium:/usr/bin/chromedriver:${PATH}"

# Switch to non-root user
USER appuser

# Reset entrypoint
ENTRYPOINT []

# Set default command
CMD ["python", "src/main.py"]