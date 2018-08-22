## Starting locally

./run_docker.sh will auto-detect whether or not you are in AWS or not.  If no, it will start the containers with only HTTP.

## Starting in AWS

./run_docker.sh will auto-detect whether or not you are in AWS or not.  If yes, it will start the containers with both HTTP and HTTPS.  The SSL certificate will be generated if it doesn't exist, otherwise it will check it if the SSL certificate needs to be updated.

## Deploying onto a new Host

There is a systemd service called update_cert that runs every evening at 6pm to check to see if the cert needs to be updated yet, as it's only valid for 3 months.  These service files need to be put into place and started.  To do that, run "./deploy.sh" and it will copy the files to the right place and start the service.

If you want to see the logs for the service, run "sudo journalctl -u update_cert"
