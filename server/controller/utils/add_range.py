#!/usr/bin/python3

import controller

start = input("First 3 octets (172.16.2): ")
end = input("End of range (255): ")

ips = []

for i in range(1, int(end)):
    ips.append(start + '.' + str(i))

print("Adding " + str(len(ips)) + " addresses to member.")

controller.add_range(input("Member: "), "7a3a04c8a8ee2179", ips)
