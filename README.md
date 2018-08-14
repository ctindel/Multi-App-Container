A fork of 
https://github.com/ericcgu/Flask_Dash_Container

Added extra items to requirements.txt in order to get this to correctly build and run.
Demos a sample StockTicker app (renamed app.py) which originated 
on [Jose Portilla's Dash course in Udemy](https://www.udemy.com/interactive-python-dashboards-with-plotly-and-dash/learn/v4/overview).

## Multi-App-Container 

This is essentially a fork of the Stock Ticker with two apps now. Second one is Eric's simple graph.

    dash1:
            container_name: dash1
                restart: always
                build: ./dash1
                ports:
                - "8500:8500"
                command: gunicorn -w 1 -b :8500 app1:server

## Synopsis
A Nginx and Python Flask Container used for bootstraping continuous deployment of Dash / Plot.ly Applications.
Requires :


    
    

## What is Dash? mmmm

Dash Web Applications combine the full power and best features of Plot.ly, Python, React.js and Flask.

https://dash.plot.ly/gallery

## Code Example

/bin/bash run_docker.sh

1. It will kill all running docker processes.
2. Will start all required containers in background

### Preview

http://localhost:8000/


## Installation

Requires Docker and Docker Compose

## Run on EC2

Launch micro-T2.micro Ubuntu image.

Get ssh keys

SSH in and 

Install 
* git
* docker
* docker-compose

git clone (this repo) in a directory of your choice `(/home/ubuntu/your_playground)`

Once successfullly cloned

There will be a run_docker.sh file where you cloned into.

Run it as such:

`/etc/bash run_docker.sh`

From a web browser:

hit your `ec2_public_address:8000`    

add 8000 for the port

The app is a stock plotter using Dash.
It grabs price info from IEX using pandas_datareader.
The dropdown stock symbors are populated by reading in the NASDAQ ticker symbols from a file in the same directory.





