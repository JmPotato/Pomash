# syntax=docker/dockerfile:1

FROM python:3.11.7

WORKDIR /pomash_deployment

COPY . .

RUN chmod +x deploy.sh

CMD ["./deploy.sh", "5299"]
