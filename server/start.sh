#!/bin/bash

echo "Starting Constellation Controller..."

screen -S controller -dm ./controller.sh
screen -S caddy -dm ./caddy.sh

screen -ls

echo "DONE"
