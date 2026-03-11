# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies required for transformers/torch
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY app.py .

# Create a non-root user to run the application
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Command to run the application
CMD ["python", "app.py"]