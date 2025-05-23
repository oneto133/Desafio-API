FROM python:3.13-slim-buster

WORKDIR /app

COPY requeriments.txt .

RUN pip install --no-cache-dir -r requeriments.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.main.py", "--host", "0.0.0.0", "--port", "8000"]