FROM sagemath/sagemath:10.7

RUN sage -python -m pip --no-cache-dir install pycryptodome

USER root
RUN apt-get update && \
    apt-get install -y --no-install-recommends xinetd && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /home/sage
COPY --chown=sage:sage --chmod=0700 src/ .
COPY --chown=root:root --chmod=0400 ctf.xinetd /etc/xinetd.d/ctf

CMD [ "/home/sage/run.sh" ]

EXPOSE 9999
