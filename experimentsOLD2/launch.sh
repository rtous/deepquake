#!/bin/bash
#EXAMPLE: ./experiments/launch.sh ./experiments/experiment_6_train.sh K3 data1 10

INPUT=""
for var in "$@"
do
    INPUT=$INPUT" "$var
done
echo $INPUT
sh $INPUT




