# Use Python 3.12 official image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy datasets folder
COPY datasets/ ./datasets/

# Copy models folder
COPY models/ ./models/

# Copy application code (this includes templates if they exist)
COPY . .

# Create templates and static directories if they don't exist
RUN mkdir -p templates static

# Expose port (Railway will set PORT env var)
EXPOSE ${PORT:-5000}

# Run the application
CMD ["python", "main.py"]
