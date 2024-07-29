FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY src src
COPY src/api/app.py app.py

CMD ["python", "app.py"]
