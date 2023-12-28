FROM python:3.10.13-alpine


WORKDIR /app

RUN apk update \
    && apk upgrade \
    && apk add --no-cache \
        gcc \
        gettext \
        musl-dev \
        mysql-client \
        mariadb-connector-c-dev \
        libffi-dev \
        openssl-dev \
        py3-pip \
        python3 \
        python3-dev


COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/app/docker-entrypoint.sh"]