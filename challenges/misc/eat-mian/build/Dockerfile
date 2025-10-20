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
RUN cd qemu && patch linux-user/syscall.c < patch.diff && \
    ./configure --target-list=x86_64-linux-user --static && \
    make -j8

FROM python:3.13-alpine

RUN pip3 --no-cache-dir install fastapi "uvicorn[standard]" PyNaCl && apk add build-base libseccomp linux-headers make automake wget automake unzip gperf

RUN adduser -D -h /app app

WORKDIR /app

COPY --from=builder --chmod=0755 /build/qemu/build/qemu-x86_64 /usr/local/bin
COPY --chown=app:app --chmod=0700 app/ .

CMD [ "/app/run.sh" ]
