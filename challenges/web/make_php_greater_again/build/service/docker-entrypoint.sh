#!/bin/bash

rm -f /docker-entrypoint.sh

if [ -z "$GZCTF_FLAG" ]; then
    export GZCTF_FLAG="susctf{testflag}"
fi

echo "$GZCTF_FLAG" >/flag

php-fpm &
nginx &

echo "Running..."

tail -F /var/log/nginx/access.log /var/log/nginx/error.log
