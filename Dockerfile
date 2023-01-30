# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /pomash_deployment

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt


COPY . .

RUN python3 init_db.py

CMD ["python3", "run.py" , "--port=5299"]
