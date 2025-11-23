FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install flask mysql-connector-python

EXPOSE 3000

CMD ["python3", "app.py"]

