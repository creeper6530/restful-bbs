#!/bin/bash
clear
docker compose down flask-app
docker compose build flask-app
docker compose up -d