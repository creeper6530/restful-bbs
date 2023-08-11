#!/bin/bash
clear
docker compose down
docker compose build flask-app
docker compose up -d