#!/usr/bin/python3
from flask import Flask, request, render_template, Markup, redirect, make_response, Response
import os
import datetime
import json
import domains
import authentication
import controller

NETWORK = controller.NETWORK

application = Flask(__name__, static_url_path="/static")

@application.route("/network/")
def index():
    return render_template("index.html")

def updates():
    with open("db/updates.json", 'r') as updatefile:
        UPDATES = json.load(updatefile)
    out = ""

    for update in UPDATES:
        out += """
        <div class="wrapper">
            <small class="text-muted">""" + UPDATES[update]["date"] + """</small>
            <p class="font-weight-semibold text-gray mb-0"><a href=\"""" + UPDATES[update]["link"] + """\" style="color: black;">""" + update + """</a></p>
            <hr>
        </div>
        """

    return out

@application.route("/network/authorize")
def authorize():
    member = request.args["member"]
    if member:
        controller.authorize(request.args["member"], NETWORK)
        return redirect("/network/dashboard")
    else:
        return render_template("alert.html", alert="Invalid Member ID.")

@application.route("/network/unauthorize")
def unauthorize():
    member = request.args["member"]
    if member:
        controller.unauthorize(request.args["member"], NETWORK)
        return redirect("/network/dashboard")
    else:
        return render_template("alert.html", alert="Invalid Member ID.")

@application.route("/network/name", methods=["GET", "POST"])
def name():
    if request.method == "GET":
        return """
            <!DOCTYPE html>
                <form action='/network/name' method='POST'>
                    Name: <input type='text' name='name'>
                    <br>
                    Address: <input type='text' name='address' value='""" + request.args.get("address") + """'>
                    <input type='submit'>
                </form>
            </html>
            """
    elif request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        controller.addName(name, address)
        return redirect("/network/dashboard")


@application.route("/network/delete", methods=["GET"])
def delete():
    return request.args.get("address")


@application.route("/network/dashboard")
def dashboard():
    members_str = ""
    routes = ""
    addresses = 0
    authorized_members = 0
    records = 0
    for domain in domains.db:
        for record in domains.db[domain]["records"]:
            records += 1
    for member in controller.members(NETWORK):
        member = controller.member_lookup(member, NETWORK)
        online = "UNKNOWN"
    #    for peer in controller.peers():
     #       if peer["address"] == member["id"]: # Find the correct member in the peers list
 #               ip = peer["paths"][0]["address"]
     #           online = "<a style='color: green;'>Online</a>"
            #else:
                #ip = "N/A"
                #online = "<a style='color: red;'>Offline</a>"

        if member["authorized"]:
            auth = "<a style='color: green;' href='/network/unauthorize?member=" + member["id"] + "'>Authorized</a>"
        else:
            auth = "<a style='color: red;' href='/network/authorize?member=" + member["id"] + "'>Unauthorized</a> <a style='color: red; font-weight: bold;' href='/network/delete?address=" + member["id"] + "'>Delete</a>"

        try:
            membername = controller.name(member["address"])
        except KeyError:
            membername = "<a href='/network/name?address=" + member["address"] + "'><i>Unknown</i></a>"

        members_str += """
                <tr>
                    <td>""" + membername + """</td>
                    <td>""" + member["address"] + """</td>
                    <td><u>""" + str(member["ipAssignments"]).strip("['").strip("']").replace("', '", "</u>, <u>") + """</b></td>
                    <td>""" + str(member["vMajor"]) + '.' + str(member["vMinor"]) + '.' + str(member["vProto"]) + '.<small>' + str(member["vRev"]) + """</small></td>
                    <td>""" + auth + """</td>
                    <td>""" + online + """</td>
                </tr>
                """

        if member["authorized"]:
            authorized_members += 1

        for ip in member["ipAssignments"]:
            addresses += 1

    for route in controller.network_lookup(NETWORK)["routes"]:
        routes += "<h6 class='font-weight-light mb-4'>" + str(route["target"]) + "</h6>"

    try:
        records_avg = int(records/len(domains.db))
    except ZeroDivisionError:
        records_avg = 0
    
    domains_str = ""

    for domain in domains.db:
        domains_str += """
            <tr>
                <td><a style='color: black;' href='/network/manage?domain=""" + str(domain) + """'>""" + str(domain) + """</a></td>
                <td>""" + str(domains.db[domain]["records"]) + """</td>
                <td>""" + str(domains.db[domain]["token"]) + """</td>
            </tr>
        """

    return render_template("dashboard.html", username="spdr",
                                             email="Arachnid Controller",
                                             domains=len(domains.db),
                                             addresses=addresses,
                                             records=records,
                                             records_avg=records_avg,
                                             members=len(controller.members(NETWORK)),
                                             tlds=len(domains.tlds),
                                             blocks=len(controller.network_lookup(NETWORK)["ipAssignmentPools"]),
                                             authorized_members=authorized_members,
                                             members_str=Markup(members_str),
                                             network=NETWORK,
                                             network_name=controller.network_lookup(NETWORK)["name"],
                                             routes=Markup(routes),
                                             updates=Markup(updates()),
                                             hosts=domains.hosts(),
                                             domains_str=Markup(domains_str)
                                             )

@application.route("/network/search", methods=["GET", "POST"])
def search():
    if request.method == "GET":
        return render_template("search.html", domains="", tlds=domains.get_tlds())
    elif request.method == "POST":
        return render_template("search.html", domains=Markup(domains.search_domain(request.form["query"])),
                               tlds=domains.get_tlds(), alert=Markup(domains.alert))

@application.route("/network/manage", methods=["GET"])
def manage():
    domain = request.args.get("domain")
    if domain and domain in domains.db:
        return render_template("dns.html", domain=request.args.get("domain"), records=Markup(domains.records(request.args.get("domain"))))
    elif domain == None:
        return render_template("manage.html")
    else:
        return render_template("alert.html", alert="Domain not found.")

@application.route("/network/register", methods=["GET"])
def regiser():
    domain = request.args.get("domain")
    if domain:
        if domain not in domains.db:
            return render_template("register.html", domain=domain, token=domains.register(domain))
        else:
            render_template("alert.html", alert="Domain " + domain + " already registered.")
    else:
        return redirect("/networ/search")

@application.route("/network/prompt", methods=["GET"])
def prompt():
    domain = request.args.get("domain")
    if domain:
        return render_template("prompt.html", domain=domain)
    else:
        return redirect("/network/search")

@application.route("/network/record", methods=["GET", "POST"])
def record():
    if request.method == "GET":
        return redirect("/network/search")
    elif request.method == "POST":
        try:
            name = request.form.get("name")
            address = request.form.get("addr")
            domain = request.form.get("domain")
            token = request.form.get("token")


            if token == domains.db[domain]["token"]:
                if name and (name.isalnum() or name == '@') and domains.inRange(address):
                    domains.add_record(domain, name, address)
                else:
                    return render_template("dns.html", domain=domain, records=Markup(domains.records(domain)), alert="Invalid DNS Entry. Please try again.")
            else:
                return render_template("dns.html", domain=domain, records=Markup(domains.records(domain)), alert="Invalid DNS Entry. Please try again.")
        except:
            return render_template("alert.html", alert="DNS record update failed. Please try again.")
    return render_template("dns.html", domain=domain, records=Markup(domains.records(domain)))

@application.route("/network/access", methods=["GET", "POST"])
def access():
    if request.method == "GET":
        return Redirect("/network/")
    elif request.method == "POST":
        mac = request.form["mac"]
        id = request.form["id"]

        os.system("echo Client " + id + " requested access with MAC: " + mac + " >> alerts.txt")
        return render_template("alert.html", alert="Device authorization request complete.", text="Please allow up to 24 hours for the request to be processed.")

@application.route("/network/hosts", methods=["GET"])
def hosts():
    if request.environ['REMOTE_ADDR'] == "127.0.0.1": # only allow localhost
        resp = make_response(domains.hosts())
        resp.mimetype = 'text/plain'
        return resp

@application.route("/network/address")
def address():
    return str(NETWORK)


if __name__ == '__main__':
    application.run(host='localhost', port=8080, debug=False)
