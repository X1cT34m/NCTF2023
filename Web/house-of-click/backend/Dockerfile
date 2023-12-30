FROM golang:1.21 AS builder

COPY ./readflag.go /app/readflag.go

WORKDIR /app

RUN go build readflag.go

FROM python:3.11

COPY ./src /app

COPY --from=builder /app/readflag /readflag

WORKDIR /app

RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple web.py clickhouse_connect gunicorn && \
    echo -n $(cat /dev/urandom | head -n 10 | md5sum | head -c 32) > /app/.token && \
    mkdir /app/upload && \
    chmod -R 777 /app/upload /app/templates && \
    echo nctf{hacking_clickhouse_database_qkh7ZrPqHK2GVHky} > /flag && \
    groupadd -r app && \
    useradd -r -g app app && \
    chmod 400 /flag && \
    chmod 4755 /readflag

USER app

CMD gunicorn -w 4 -b 0.0.0.0:8001 run:application