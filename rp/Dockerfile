FROM debian:buster-slim

RUN apt-get update -qq && \
  apt-get install -y --no-install-recommends \
  python3 virtualenv python3-virtualenv \
  uwsgi uwsgi-plugin-python3

RUN mkdir -p /rp
WORKDIR /rp
RUN virtualenv -p /usr/bin/python3 venv
ENV PATH ./venv/bin:$PATH
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY app/ ./app
COPY run.sh uwsgi.ini ./
COPY certs/ ./certs/

EXPOSE 8443
CMD ["./run.sh"]
