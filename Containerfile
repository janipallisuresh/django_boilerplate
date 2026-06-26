FROM python:3.10

WORKDIR /app

# Install system build dependencies (needed for some packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    python3-setuptools \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip tooling
RUN pip install --upgrade pip setuptools wheel && \
    pip install setuptools==68.0.0

# Install the rest of your requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
