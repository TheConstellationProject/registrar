#!/bin/bash
# Constellation Network Controller init script

# Start controller and registrar server
/home/controller/.local/bin/gunicorn -w 2 -b localhost:8080 --chdir controller/ server

