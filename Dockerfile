FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "main.py"]
