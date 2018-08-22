#!/bin/bash

get_cert() {
    docker run --rm \
        -v /etc/letsencrypt/etc:/etc/letsencrypt \
        -v /etc/letsencrypt/www:/var/www \
        webdevops/certbot /usr/bin/certbot certonly \
        --non-interactive \
        --agree-tos \
        --webroot \
        -w /var/www \
        -m "steve@thoughtsociety.org" \
        -d "www.tsworker.com,tsworker.com" 
        #--staging
}

update_cert() {
    docker run --rm \
        -v /etc/letsencrypt/etc:/etc/letsencrypt \
        -v /etc/letsencrypt/www:/var/www \
        webdevops/certbot /usr/bin/certbot renew --non-interactive
       # webdevops/certbot /usr/bin/certbot renew --staging --non-interactive
}

# Device Mapper Bug will fill up the available space in the docker pool 
#  as shown by docker info
# https://stackoverflow.com/questions/27853571/why-is-docker-image-eating-up-my-disk-space-that-is-not-used-by-docker
docker system prune -f
docker image prune -f
docker volume prune -f
docker container prune -f
#check_run_cmd "docker ps -qa | xargs docker inspect --format='{{ .State.Pid }}' | xargs -IZ fstrim /proc/Z/root/"

if [ ! -e "/etc/letsencrypt/etc/live/www.tsworker.com/privkey.pem" ]; then
    echo "Getting certificates..."
    get_cert
else
    echo "Updating certificates..."
    update_cert
fi

# If the cert is updated we need to tell nginx to reload so it will see the new certs
docker exec nginx nginx -s reload
