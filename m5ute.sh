#!/bin/bash
cd "$(dirname "$(readlink -f "$0")")"
nohup python main.py 2> m5ute.log &
