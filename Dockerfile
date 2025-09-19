FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install pipx via pip
RUN pip install --no-cache-dir pipx \
    && pipx install uv

# Make sure pipx-installed tools are on PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy project files
COPY ./ ./

# Install project dependencies via uv
RUN uv sync

EXPOSE 8501

# Healthcheck
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
ENTRYPOINT ["uv","run","-m","streamlit","run","main.py","--server.port=8501","--server.address=0.0.0.0"]
