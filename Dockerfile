# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables for Python to run in optimized mode
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc make && \
    rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /app

# Copy only the necessary files for dependency installation
COPY pyproject.toml poetry.lock Makefile /app/

# Install dependencies
RUN make build

# Copy application config
COPY ./config /app/config

# Copy standard utilities
COPY ./utils /app/utils

# Copy the prediction model
COPY ./staged/clf.pkl /app/staged/clf.pkl

# Copy application server code
COPY ./server /app/server

# Check model hash
RUN make checkmodelhash

# Test the deployment
RUN make test

# Expose the application port
EXPOSE 8000

# Run the application
CMD ["make", "runserver"]
