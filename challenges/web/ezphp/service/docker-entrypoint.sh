#!/bin/bash

rm -f /docker-entrypoint.sh

echo "$GZCTF_FLAG" | tee "/flag-$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)"
export GZCTF_FLAG=""

php-fpm &
nginx &

echo "Running..."

tail -F /var/log/nginx/access.log /var/log/nginx/error.log
