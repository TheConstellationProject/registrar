#!/usr/bin/python3
import json
import requests

class Status:
    ERROR = "\033[91m[⚠]\033[0m"
    SUCCESS = "\033[92m[✓]\033[0m"
    INFO = "\033[94m[ℹ]\033[0m"

memberdb = {}

try:
    with open("db/token.txt", "r") as authfile:
        _HEADERS = {"X-ZT1-Auth": authfile.read().strip()}

    with open("db/network.txt", "r") as netfile:
        NETWORK = netfile.read().strip()
except PermissionError:
    print(Status.ERROR + " ERROR: Permission to read authtoken denied.")
    exit(1)

_STATUS = requests.get("http://localhost:9993/status", headers=_HEADERS).json()
_ADDRESS = _STATUS["address"]
_VERSION = _STATUS["version"]

def status():
    r = requests.get("http://localhost:9993/controller", headers=_HEADERS).json()
    print(Status.INFO + " ZeroTier Controller v" + str(r["apiVersion"]))
    networks = requests.get("http://localhost:9993/controller/network/", headers=_HEADERS).json()
    for network in networks:
        network = requests.get("http://localhost:9993/controller/network/" + network, headers=_HEADERS).json()
        print(network["name"] + " " + network["id"] + " " + "[PRIVATE]") if network["private"] else print("[PUBLIC]")
        for range in network["ipAssignmentPools"]:
            print("\t" + range["ipRangeStart"] + "-" + range["ipRangeEnd"])
        print()
        for member in members(network["id"]):
            r = requests.get("http://localhost:9993/controller/network/" + network["id"] + "/member/" + member, headers=_HEADERS).json()
            print(r["address"] + " " + str(r["ipAssignments"]) + " (" + str(r["vMajor"]) + '.' + str(r["vMinor"]) + '.' + str(r["vProto"]) + ')')

def create(name, private=True):
    r = requests.post("http://localhost:9993/controller/network/" + _ADDRESS + "______", json={"name": name,
                                                                                               "private": private,
                                                                                               "v4AssignMode": {"zt": True},
                                                                                               "v6AssignMode": {"zt": True},

                                                                                               "routes": [
                                                                                                   {'target': '172.16.0.0/16', 'via': None},
                                                                                                   {'target': 'fd00:1337::/32', 'via': None}
                                                                                                   ],

                                                                                               "ipAssignmentPools": [
                                                                                                   {
                                                                                                       "ipRangeStart": "172.16.0.1",
                                                                                                       "ipRangeEnd": "172.16.255.255"
                                                                                                   },

                                                                                                   {
                                                                                                        "ipRangeStart": "fd00:1337::",
                                                                                                        "ipRangeEnd": "fd00:1337:ffff:ffff:ffff:ffff:ffff:ffff"
                                                                                                   }
                                                                                                   ]
                                                                                                }, headers=_HEADERS)
    return r.json()["id"]


def delete(address):
    return requests.delete("http://localhost:9993/controller/network/" + address, headers=_HEADERS).json()

def members(network):
    return list(requests.get("http://localhost:9993/controller/network/" + network + "/member/", headers=_HEADERS).json().keys())

def member_lookup(member, network):
    return requests.get("http://localhost:9993/controller/network/" + network + "/member/" + member, headers=_HEADERS).json()

def network_lookup(network):
    return requests.get("http://localhost:9993/controller/network/" + network, headers=_HEADERS).json()

def authorize(member, network):
    return requests.post("http://localhost:9993/controller/network/" + network + "/member/" + member, json={"authorized": True}, headers=_HEADERS).json()

def unauthorize(member, network):
    return requests.post("http://localhost:9993/controller/network/" + network + "/member/" + member, json={"authorized": False}, headers=_HEADERS).json()

def peers():
    return requests.get("http://localhost:9993/peer", headers=_HEADERS).json()

def add_range(member, network, addrs):
    return requests.post("http://localhost:9993/controller/network/" + network + "/member/" + member, json={"ipAssignments": list(addrs)}, headers=_HEADERS).json()

def name(member):
    with open("db/members.json", "r") as memberfile:
        memberdb = json.load(memberfile)
    return memberdb[member]

def addName(name, member):
    with open("db/members.json", "r") as memberfile:
        memberdb = json.load(memberfile)

    memberdb[member] = name
    with open("db/members.json", "w") as memberfile:
        memberfile.write(json.dumps(memberdb))

def deleteMember(member, network):
    return requests.delete("http://localhost:9993/controller/network/" + network + "/member/" + member, headers=_HEADERS).json()

if __name__ == '__main__':
    status()
