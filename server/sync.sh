#!/bin/bash
echo "Syncing..."
curl -s http://localhost:8080/network/hosts > hosts.conf
echo "DONE"
