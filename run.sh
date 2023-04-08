#!/bin/bash
for i in {1..10000}
do
   etcdctl put test_$i hello_world_$i
done