#!/usr/bin/env bash

source ./utils/utils.sh

echo "killing old docker processes"
docker-compose -f docker-compose.yml rm -fs

echo "building docker containers"
docker-compose -f docker-compose.yml up --build -d

# If the cert hasn't been generated yet, we can't start nginx with the 
#  SSL config because it will fail.  So in the case where nothing
#  exists we will start nginx without SSL, then generate or update
#  the cert, copy it into the container, and reload nginx.
#
# Separately, there is a systemd service which will periodically
#  also run the update_cert to check for updates
./utils/update_cert.sh
check_run_cmd "docker cp ./nginx/nginx.https.conf nginx:/etc/nginx/conf.d/"
check_run_cmd "docker exec nginx nginx -s reload"
