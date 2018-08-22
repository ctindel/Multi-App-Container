#!/usr/bin/env bash

is_aws=false

if [ -f /sys/hypervisor/uuid ] && [ `head -c 3 /sys/hypervisor/uuid` == ec2 ]; then
    is_aws=true
fi

if [ $is_aws = false ]; then
    echo "We are not running on AWS"
    bash ./run_docker_local.sh
else
    echo "We are running on AWS"
    bash ./run_docker_aws.sh
fi
