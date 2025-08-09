FROM python:3.11-slim

WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code
COPY . .

# Ensure the start script is executable
RUN chmod +x start.sh

# Expose the API port
EXPOSE 8000

# Set entrypoint to run the seeder followed by the FastAPI server
CMD ["./start.sh"]
