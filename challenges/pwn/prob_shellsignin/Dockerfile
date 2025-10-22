FROM ubuntu:20.04

RUN apt update && apt install -y xinetd

COPY --chmod=755 pwn /pwn
COPY xinetd.conf /etc/xinetd.conf
COPY --chmod=755 run.sh /run.sh

CMD ["bash", "/run.sh"]
