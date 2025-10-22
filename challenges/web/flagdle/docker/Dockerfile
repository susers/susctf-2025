FROM alpine:3

RUN apk update && apk add lighttpd

COPY ./dist /var/www/localhost/htdocs
COPY lighttpd.conf /etc/lighttpd

CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
