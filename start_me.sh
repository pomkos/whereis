#!/bin/bash
# For use with crontab
source ~/miniconda3/bin/activate

cd $HOME/projects/whereis
conda activate whereis_env # activate the new conda env
nohup streamlit run whereis.py --server.port 8502 & # run in background
nohup streamlit run settings.py --server.port 8503 & # run in background

echo "Running settings.py on port 8502!"
echo "Running settings.py on port 8503!"
