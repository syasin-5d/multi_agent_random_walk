#!/bin/sh

file_name=08_linklist.txt
a=1
nagents=10
T=1000

for b in 2 100 1000
do
    python R12.py --file_name $file_name -a $a -b $b --nagents=$nagents -T $T
done
