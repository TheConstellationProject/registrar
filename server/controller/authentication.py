import hashlib
import json
import getpass

def getHash(string):
    return str(hashlib.sha512(string.encode()).hexdigest())

db = {}

def sync():
    global db
    with open("db/passwd.json", 'r') as pswdfile:
        db = json.load(pswdfile)

def dump():
    global db
    with open("db/passwd.json", 'w') as pswdfile:
        pswdfile.write(json.dumps(db))

def authenticate(user, pswd):
    try:
        return db[user] == getHash(pswd)
    except KeyError:
        return False

sync()

if __name__ == '__main__':
    uname = input("Username: ")
    db[uname] = getHash(getpass.getpass("Password: "))
    dump()
