#!/bin/bash

if [ -z "$GZCTF_FLAG" ]; then
    export GZCTF_FLAG="susctf{testflag}"
fi

echo "$GZCTF_FLAG" >/flag-"$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 16 | head -n 1)"
export GZCTF_FLAG=""

service postgresql start

flask run --host=0.0.0.0
