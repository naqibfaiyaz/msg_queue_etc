#!/bin/bash

export FLASK_APP=run.py
export FLASK_ENV=development
export RANGE_START=0
export RANGE_END=45
export ETCD_HOST='67.205.137.130:2379,143.198.161.94:2379,143.198.162.212:2379'


./.venv/Scripts/python.exe run.py --start ${1} --end ${2} >> log.txt 2>&1 &
