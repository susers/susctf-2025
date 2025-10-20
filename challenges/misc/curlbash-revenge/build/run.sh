#!/bin/sh

if [ -z "$GZCTF_FLAG" ]; then
    export GZCTF_FLAG="susctf{testflag}"
fi

echo "$GZCTF_FLAG" >/flag
export GZCTF_FLAG=""
echo "Blocked by ctf_xinetd" >/etc/banner_fail

chmod 444 /flag

inetd -f
sleep infinity
