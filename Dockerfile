FROM python:alpine

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app.py .

CMD quart run --host 0.0.0.0