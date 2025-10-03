#!/bin/bash

if [ ! -f ".env" ]; then
    cp enviroment .env
fi

# docker rm -f postgres_data
docker-compose up