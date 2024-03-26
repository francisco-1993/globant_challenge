FROM python:3.11-slim

WORKDIR /app

#RUN apt-get update && apt-get install -y libpq-dev

#EXPOSE 5432/tcp

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]