#!/usr/bin/env bash

for((db = 0; db<=9; db++))
do
qsub Regular.sh Regular.py 500 100 $db
done
