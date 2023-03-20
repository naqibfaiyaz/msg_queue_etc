#!/bin/bash

export FLASK_APP=run.py
export FLASK_ENV=development
export RANGE_START=0
export RANGE_END=45
export ETCD_HOST='10.0.0.72:2379,10.0.0.56:2379,10.0.0.87:2379'


python3 run.py --start ${1} --end ${2}
