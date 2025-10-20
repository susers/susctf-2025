#!/bin/sh

echo $GZCTF_FLAG >/flag
export GZCTF_FLAG=""

/app/am-i-admin
