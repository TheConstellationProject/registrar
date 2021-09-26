#!/usr/bin/python3
import getpass
import hashlib

username = input("Username: ")
password = getpass.getpass("Password: ")

print("\"" + username + "\": \"" + str(hashlib.sha512(password.encode()).hexdigest()) + "\"")
