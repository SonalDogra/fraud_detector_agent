FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ✅ Railway expects apps to run on port 8080
EXPOSE 8080

# ✅ Updated to match port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
