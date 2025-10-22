#!/bin/sh

echo $GZCTF_FLAG > /flag
# export GZCTF_FLAG=""
echo "Blocked by ctf_xinetd" > /etc/banner_fail

chown -R sage:sage /flag
chmod 400 /flag

/etc/init.d/xinetd start
sleep infinity
