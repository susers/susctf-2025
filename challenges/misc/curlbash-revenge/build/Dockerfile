FROM ubuntu:22.04 AS builder
WORKDIR /build
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ca-certificates wget build-essential python-is-python3 python3-venv python3-tomli ninja-build pkg-config libglib2.0-dev libpixman-1-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    wget https://download.qemu.org/qemu-10.1.0.tar.xz && \
    tar xvf qemu-10.1.0.tar.xz && mv -v qemu-10.1.0 qemu && rm -v qemu-10.1.0.tar.xz
COPY 0001-linux-user-syscall-add-sandbox.patch /build/qemu/patch.diff
RUN cd qemu && patch -p1 < patch.diff && \
    ./configure --target-list=x86_64-linux-user --static && \
    make -j8

FROM alpine:latest

RUN apk update && \
    apk add bash curl python3 py3-requests busybox-extras

WORKDIR /app

COPY --from=builder --chmod=0755 /build/qemu/build/qemu-x86_64 /usr/local/bin
COPY --chmod=0755 main.py .
COPY --chmod=0400 inetd.conf /etc/inetd.conf
COPY --chmod=0400 services /etc/services
COPY --chmod=0755 run.sh .

RUN touch /app/testscript.sh && chown nobody:nobody /app/testscript.sh && chmod -R 0400 /tmp

ENV PYTHONUNBUFFERED 1

CMD [ "/app/run.sh" ]

EXPOSE 9999
