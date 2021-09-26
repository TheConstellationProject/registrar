#!/bin/bash
# Arachnid Network Config Script
#
# This script is designed to install and configure Arachnid Network
# on Debian + systemd based systems.

install() {
	curl -s https://install.zerotier.com | bash
	sudo zerotier-cli join $(curl -S https://arachnid.cc/network/address)
	echo -e "\nPlease provide the following information to the network administrator.\n"
	status
}

connect() {
	sudo zerotier-cli join $(curl -S https://arachnid.cc/network/address)
}

restart() {
	sudo systemctl restart zerotier-cli
}

status() {
	echo Arachnid Network Connection Status
	echo ----------------------------------
	echo $(sudo zerotier-cli listnetworks | grep Arachnid | cut -d ' ' -f 4) $(sudo zerotier-cli listnetworks | grep Arachnid | cut -d ' ' -f 3)
	echo Member ID: $(sudo zerotier-cli info | cut -d ' ' -f 3)
	echo IP: $(curl -s ipinfo.io/ip)
	echo ----------------------------------
	echo
	sudo zerotier-cli listnetworks
}

if [[ $1 = "install" ]]; then
	install
	restart
elif [[ $1 = "connect" ]]; then
	connect
	restart
elif [[ $1 = "leave" ]]; then
	sudo zerotier-cli leave $(sudo zerotier-cli listnetworks | grep Arachnid | cut -d ' ' -f 3)
	restart
elif [[ $1 = "status" ]]; then
	status
elif [[ $1 = "restart" ]]; then
	restart
else
	echo "spdr.sh v3.0"
	echo Usage: ./spdr.sh [install, status, connect, leave, restart]
	echo ""
	echo "	./spdr.sh install - Install and connect to Arachnid Network"
	echo "	./spdr.sh status - Show network status"
	echo "	./spdr.sh connect - Connect to Arachnid Network"
	echo "	./spdr.sh leave - Leave Arachnid Network"
	echo "	./spdr.sh restart - Restart ZeroTier service"
fi

