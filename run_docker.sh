#!/usr/bin/env bash

is_aws=false

# This first, simple check will work for many older instance types.
if [ -f /sys/hypervisor/uuid ]; then
  # File should be readable by non-root users.
  if [ `head -c 3 /sys/hypervisor/uuid` == "ec2" ]; then
    is_aws=true
  fi
# This check will work on newer m5/c5 instances, but only if you have root!
elif [ -r /sys/devices/virtual/dmi/id/product_uuid ]; then
  # If the file exists AND is readable by us, we can rely on it.
  if [ `head -c 3 /sys/devices/virtual/dmi/id/product_uuid` == "EC2" ]; then
    is_aws=true
  fi
else
  # Fallback check of http://169.254.169.254/. If we wanted to be REALLY
  # authoritative, we could follow Amazon's suggestions for cryptographically
  # verifying their signature, see here:
  #    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-identity-documents.html
  # but this is almost certainly overkill for this purpose (and the above
  # checks of "EC2" prefixes have a higher false positive potential, anyway).
  if $(curl -s -m 5 http://169.254.169.254/latest/dynamic/instance-identity/document | grep -q availabilityZone) ; then
    is_aws=true
  fi
fi

if [ $is_aws = false ]; then
    echo "We are not running on AWS"
    bash ./run_docker_local.sh
else
    echo "We are running on AWS"
    bash ./run_docker_aws.sh
fi
