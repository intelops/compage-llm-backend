# Stage 1: Build the application
FROM python:3.8.10-slim AS builder

WORKDIR /app

# Create and activate a virtual environment
RUN python3.8 -m venv venv
ENV PATH="/app/venv/bin:$PATH"

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run the application (if needed during build, e.g., for migrations)
RUN python main.py

# Stage 2: Create a lightweight image for running the application
FROM python:3.8.10-slim

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /app/venv /app/venv

# Set the PATH to include the virtual environment
ENV PATH="/app/venv/bin:$PATH"

# Set up the user (optional but recommended for security)
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Copy your application files (code, configurations, etc.)
COPY . .

# Specify the command to run your application
CMD ["python", "main.py"]
