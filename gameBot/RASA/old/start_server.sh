#!/bin/bash

#TODO: Test

# The goal here is to run this script using an anaconda shell
source ~/anaconda3/etc/profile.d/conda.sh
# Alternatively, this line might work:
# eval "$(conda shell.bash hook)"

conda activate alana
rasa run --enable-api --log-file server-log.log