#!/bin/bash
sudo apt update
sudo apt upgrade
sudo apt install git sudo curl zsh ufw screen python3 python3-pip dnsmasq
pip3 install flask gunicorn
sudo systemctl disable systemd-resolved
sudo systemctl stop systemd-resolved
ls -lh /etc/resolv.conf
sudo rm /etc/resolv.conf
echo "nameserver 1.1.1.1" > /etc/resolv.conf

