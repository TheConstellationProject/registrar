# domains.py
import json
import datetime
import random
import string

tlds = {}
db = {}
alert = ""


def sync():
    global tlds
    global db
    with open("db/tlds.json", 'r') as domain_file:
        tlds = json.load(domain_file)

    with open("db/db.json", 'r') as db_file:
        db = json.load(db_file)


def dump():
    global tlds
    global registar
    with open("db/tlds.json", 'w') as domain_file:
        domain_file.write(json.dumps(tlds))

    with open("db/db.json", 'w') as db_file:
        db_file.write(json.dumps(db))


def get_tlds():
    out = ""

    for tld in tlds:
        out += tld + ", "

    return out[:-2]


def add_tld(tld, provider):
    tlds[tld] = provider
    dump()


def available(domain):  # Is @param domain available?
    if domain in db:
        return "Unavailable"
    else:
        return "<a href='/network/prompt?domain=" + domain + "'>Available</a>"


def search_domain(search_string):
    global alert
    alert = ""
    out = ""

    try:
        domain_part = search_string.split('.')[0]
    except IndexError:
        domain_part = search_string
    else:
        try:
            tld_part = search_string.split('.')[1]
        except IndexError:
            tld_part = ""

    if tld_part in tlds:  # If the tld is valid...
        out += """
            <tr>
                <td>""" + search_string + """</td>
                <td>""" + available(domain_part + '.' + tld_part) + """</td>
            </tr>
               """
    else:  # If the tld isn't valid...
        if tld_part:
            alert = "TLD \"" + tld_part + "\" isn't valid."
        for tld in tlds:  # List out the valid tlds.
            out += """
                <tr>
                    <td>""" + domain_part + '.' + tld + """</td>
                    <td>""" + available(domain_part + '.' + tld) + """</td>
                </tr>
                   """
    return out


def get_time():
    return '{0:%I:%M%P and %S seconds. %m/%d/%Y}'.format(datetime.datetime.now())


def token():
    return "".join(random.choice(string.ascii_letters + string.digits) for i in range(32))

def register(domain):
    newtoken = token()
    db[domain] = {
        "token": newtoken,
        "date": get_time(),
        "records": {}
    }
    dump()
    return newtoken

def records(domain):
    try:
        out = ""
        for record in db[domain]["records"]:
            out += "<tr><td>" + record + "</td><td>" + db[domain]["records"][record] + "</td></tr>"

        return out

    except KeyError:
        return

def add_record(domain, name, address):
    db[domain]["records"][name] = address
    dump()

def hosts():
    out = "# Constellation Network (ConstellationNet) Hosts file.\n# Authoritative DNS servers located at 10.0.1.2 and 10.0.1.3\n"
    for domain in db:
        for record in db[domain]["records"]:
            if record == '@':
                out += db[domain]["records"][record] + "\t" + domain
            else:
                out += db[domain]["records"][record] + "\t" + record + '.' + domain

            out += "\n"
    return out

def inRange(addr):
    a = addr.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True

sync()
