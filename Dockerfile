FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed to build Python packages
RUN apt-get update && apt-get install -y \
    build-essential \       # for compiling packages like asyncpg
    libpq-dev \             # PostgreSQL client headers
    libssl-dev \            # for cryptography
    curl \                  # optional, useful for network commands
    git \                   # optional
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 10000

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:$PORT"]