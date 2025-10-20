FROM python:3.13-alpine

RUN pip3 --no-cache-dir install fastapi "uvicorn[standard]"

RUN adduser -D -h /app app
WORKDIR /app
COPY --chown=app:app --chmod=0700 app/ .

CMD [ "/app/run.sh" ]