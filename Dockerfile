FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080  # Optional but helpful

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
