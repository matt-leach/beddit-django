#!/bin/bash

project_name=beddit
project_name_app_server=beddit_app_server
domain=beddit.familyleach.net


conf_file=/etc/nginx/sites-available/$project_name
other_file=/etc/nginx/sites-enabled/$project_name



THIS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SOCKFILE=$THIS_DIR/../run/gunicorn.sock           
LOGFILE=$THIS_DIR/../logs/gunicorn_supervisor.log
HOMEDIR=$THIS_DIR/..

echo "upstream $project_name_app_server {" > $conf_file
echo "  server unix:$SOCKFILE fail_timeout=0;" >> $conf_file
echo "}" >> $conf_file

echo "server {" >> $conf_file
echo "    listen   80;" >> $conf_file
echo "    server_name $domain;" >> $conf_file

echo "    client_max_body_size 4G;" >> $conf_file

echo "    access_log $HOMEDIR/logs/nginx-access.log;" >> $conf_file
echo "    error_log $HOMEDIR/logs/nginx-error.log;" >> $conf_file

echo "    location /static/ {" >> $conf_file
echo "        alias   $HOMEDIR/static/;" >> $conf_file
echo "    }" >> $conf_file

echo "    location /media/ {" >> $conf_file
echo "        alias   $HOMEDIR/media/;" >> $conf_file
echo "    }" >> $conf_file

echo "    location / {" >> $conf_file
echo "        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;" >> $conf_file
echo "        proxy_set_header Host \$http_host;" >> $conf_file
echo "        proxy_redirect off;" >> $conf_file
echo "        if (!-f \$request_filename) {" >> $conf_file
echo "            proxy_pass http://$project_name_app_server;" >> $conf_file
echo "            break;" >> $conf_file
echo "        }" >> $conf_file
echo "    }" >> $conf_file
echo "}" >> $conf_file


ln -s $conf_file $other_file
