#!/bin/bash
source $HOME/miniconda3/bin/activate

echo "What would you like to do?"
echo "[1] Install whereis"
echo "[2] Add to crontab"
echo
read input

function edit_cron(){
    crontab -l > file
    echo "# start after each reboot" >> file
    echo "@reboot      $HOME/projects/whereis/start_me.sh" >> file
    crontab file
    rm file
    echo "whereis and whereadmin will start every reboot"
}

function install_whereis()
{
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

    read cron "Append whereis to crontab? [y/n] "
    echo


    if [[ $cron == "Y" || $cron == "y" ]]
    then
        edit_cron
    fi

    echo "whereis installed on port 8502"
    echo "whereadmin installed on port 8503"
}

if [[ $input == 1 ]]
then
    install_whereis
elif [[ $input == 2 ]]
then
    edit_cron
else
    echo "No option selected"
    exit 1
fi
