FROM python:3.12-slim

WORKDIR /app

# Install system dependencies needed to build Python packages
# for compiling packages like asyncpg
# PostgreSQL client headers
# for cryptography
# optional, useful for network commands
# optional

RUN apt-get update && apt-get install -y \
    build-essential \       
    libpq-dev \             
    libssl-dev \            
    curl \                  
    git \                   
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 10000

CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:$PORT"]