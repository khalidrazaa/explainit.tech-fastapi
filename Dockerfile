# Use Ubuntu 22.04 as base
FROM ubuntu:22.04

# Set working directory
WORKDIR /app

# Install Python 3.12 and build tools
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    libpq-dev \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Python 3.12
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-venv python3.12-dev python3.12-distutils && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python3.12 -m ensurepip && python3.12 -m pip install --upgrade pip

# Copy requirements and install
COPY requirements.txt .
RUN python3.12 -m pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port (Render uses $PORT)
EXPOSE 10000

# Start app with Gunicorn + Uvicorn
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:$PORT"]