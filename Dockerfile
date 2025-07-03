FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional if needed)
RUN apt-get update && apt-get install -y build-essential

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy full source code
COPY . .

# Expose port and run
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
