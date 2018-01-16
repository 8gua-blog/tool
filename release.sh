#!/usr/bin/env bash

PREFIX=$(cd "$(dirname "$0")"; pwd)
cd $PREFIX/tool

./py/release.xonsh.py


