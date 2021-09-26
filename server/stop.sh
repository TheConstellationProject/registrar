#!/bin/bash

echo "Stopping Constellation Controller..."

screen -X -S controller quit
screen -X -S caddy quit

screen -ls

echo "DONE"
