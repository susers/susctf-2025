FROM ubuntu:20.04

RUN apt update && apt install -y xinetd

COPY --chmod=755 pwn /pwn
COPY --chmod=755 ld-linux-x86-64.so.2 /ld-linux-x86-64.so.2
COPY libc.so.6 /libc.so.6
COPY xinetd.conf /etc/xinetd.conf
COPY --chmod=755 run.sh /run.sh

CMD ["bash", "/run.sh"]
