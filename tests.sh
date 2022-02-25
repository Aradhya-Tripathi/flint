#!bin/bash

error="\e[1;31m[ERROR]\e[0m"
execution="\e[0;36m[INFO]\e[0m"


echo -e "$execution Installing flint"
pip3 install .


echo -e "$execution Cloning repo"
git clone https://github.com/Aradhya-Tripathi/fire-watch.git
cd fire-watch

pip install -r requirements.txt
. ./run_server.sh &

cd ../
sleep 5s

echo -e "$execution Starting tests"
python -m unittest -v flint.tests.test_commands


# Killing server after running tests
kill $(lsof -i:8000)

# Cleaning up
rm fire-watch -rf