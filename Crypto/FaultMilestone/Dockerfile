FROM python:slim AS app
RUN pip install --no-cache-dir pycryptodome

FROM pwn.red/jail
COPY --from=app / /srv
COPY main.py /srv/app/run
RUN chmod 777 /srv/app/run
COPY secret.py /srv/app
COPY util.py /srv/app
ENV JAIL_MEM=300M JAIL_ENV_NUM=5  JAIL_TIME=30
