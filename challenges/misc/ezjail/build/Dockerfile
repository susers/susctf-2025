FROM alpine:latest AS builder
WORKDIR /build
RUN apk update && apk add gcc libc-dev linux-headers
COPY override.c .
RUN gcc -shared -fPIC -o override.so override.c -ldl

FROM alpine:latest

RUN apk update && \
    apk add bash busybox-extras python3 py3-requests

WORKDIR /app

COPY --from=builder --chmod=0755 /build/override.so .
COPY --chmod=0755 main.py .
COPY --chmod=0400 inetd.conf /etc/inetd.conf
COPY --chmod=0400 services /etc/services
COPY --chmod=0755 run.sh .

RUN touch /app/testscript.sh && chown nobody:nobody /app/testscript.sh && chmod -R 0400 /tmp

ENV PYTHONUNBUFFERED 1

CMD [ "/app/run.sh" ]

EXPOSE 9999
