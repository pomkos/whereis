#!/bin/bash

source ~/miniconda3/bin/activate

cd ~/projects/whereis
conda activate whereis_env # activate the new conda env
nohup streamlit run settings.py --server.port 8503 & # run in background

echo "Running settings.py on port 8503!"
