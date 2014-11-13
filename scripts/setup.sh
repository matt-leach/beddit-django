#!/bin/bash

project_name=beddit

source ../bin/activate

./setup_nginx.sh
./setup_supervisor.sh
pip install -r pip_requirements.txt

mkdir -p ../logs

touch ../logs/gunicorn_supervisor.log

supervisorctl reread
supervisorctl update
supervisorctl restart $project_name

service nginx restart