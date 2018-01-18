#!/usr/bin/env bash

URL=https://gitee.com/u8gua/tool/raw/master/setup

if [ "$(uname)" != "Darwin" ]; then
curl -s $URL/mac.sh | bash /dev/stdin arg1 arg2
fi
