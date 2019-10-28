FROM python:3.7-slim-buster

RUN mkdir -p /rp
WORKDIR /rp
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app/ ./app
COPY run.sh ./
COPY certs/ ./certs/

EXPOSE 5000
CMD ["./run.sh"]
