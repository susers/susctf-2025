FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POSTGRES_DB=susmarket
ENV POSTGRES_USER=sus
ENV POSTGRES_PASSWORD=susctf@2025

RUN apt-get update && apt-get install -y \
    postgresql postgresql-contrib sudo \
    gcc postgresql-server-dev-all \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install Flask "psycopg[binary]" psycopg_pool

COPY init.sql /tmp/init.sql

# Setup the database cluster first time, then start postgres and run init.sql
RUN service postgresql start && \
    sudo -u postgres psql --command "CREATE USER ${POSTGRES_USER} WITH SUPERUSER PASSWORD '${POSTGRES_PASSWORD}';" && \
    sudo -u postgres psql --command "CREATE DATABASE ${POSTGRES_DB} OWNER ${POSTGRES_USER};" && \
    sudo -u postgres psql -d ${POSTGRES_DB} -f /tmp/init.sql && \
    service postgresql stop

COPY src .

EXPOSE 5000

ENTRYPOINT ["/app/run.sh"]
