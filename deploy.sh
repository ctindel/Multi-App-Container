#!/bin/bash

readonly BASE_DIR=$PWD

#echo "BASE_DIR is $BASE_DIR"
sudo cp ./utils/update_cert.{service,timer} /etc/systemd/system
echo "ExecStart=/bin/bash $BASE_DIR/utils/update_cert.sh" | sudo tee -a /etc/systemd/system/update_cert.service > /dev/null
sudo systemctl enable update_cert
sudo systemctl start update_cert
