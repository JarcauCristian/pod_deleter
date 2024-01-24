FROM python:3.11-alpine

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV NAMESPACE = ""

EXPOSE 8000

CMD ["python3", "main.py"]
