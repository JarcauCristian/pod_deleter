FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 49152

CMD ["python3", "main.py"]
