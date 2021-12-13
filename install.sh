#!/bin/bash
source $HOME/miniconda3/bin/activate

sudo apt -y install tesseract-ocr
sudo apt -y install libtesseract-dev

conda create -y --name "whereis_env"
conda activate whereis_env
conda install -y -c conda-forge python=3.8
cd $HOME/projects/whereis
pip install --no-input -r requirements.txt
python db_reset.py # initiate database
echo " " >> data/home_message.txt
nohup streamlit run whereis.py --server.port 8502 &
nohup streamlit run settings.py --server.port 8503 &
conda deactivate

echo "whereis installed on port 8502"
echo "whereadmin installed on port 8503"
