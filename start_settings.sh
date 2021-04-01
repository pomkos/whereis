#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh

cd ~/projects/whereis
conda activate travel_env # activate the new conda env
nohup streamlit run settings.py --server.port 8513 & # run in background

echo "Running settings.py on port 8513!"