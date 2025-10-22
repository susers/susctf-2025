#!/bin/sh

if [ -z "$GZCTF_FLAG" ]; then
    GZCTF_FLAG="susctf{test}"
fi

echo "$GZCTF_FLAG" >/flag
export GZCTF_FLAG=""

httpd-foreground
