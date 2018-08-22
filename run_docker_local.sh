#!/usr/bin/env bash

echo killing old docker processes
docker-compose -f docker-compose-local.yml rm -fs

echo building docker containers
docker-compose -f docker-compose-local.yml up --build -d
