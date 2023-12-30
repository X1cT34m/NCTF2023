FROM golang:1.21 AS builder

COPY ./readflag.go /app/readflag.go

WORKDIR /app

RUN go build readflag.go

FROM openjdk:8

COPY ./src /app

COPY --from=builder /app/readflag /readflag

WORKDIR /app

RUN echo nctf{rce_with_evil_inlong_tubemq_server_hVu24UtFPpjsE4Dh} > /flag && \
    groupadd -r app && \
    useradd -r -g app app && \
    chmod 400 /flag && \
    chmod 4755 /readflag

USER app

CMD java -javaagent:SimpleRasp.jar -jar EvilMQ.jar