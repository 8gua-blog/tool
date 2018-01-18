#!/usr/bin/env bash

URL=https://gitee.com/u8gua/tool/raw/master/setup

SCRIPT=""

if [ "$(uname)" == "Darwin" ]; then
SCRIPT=mac
fi

if ! [ $SCRIPT == "" ]; then
curl -s $URL/$SCRIPT.sh | bash /dev/stdin arg1 arg2
fi
