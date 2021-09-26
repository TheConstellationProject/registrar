import requests

# r = requests.post("http://localhost:8080/edit/test.com/test", headers={
#     "token": "1324563u45083680u"
# })
#
# print(r.text)

def register():
    r = requests.post("http://localhost:8080/register", data={"domain": "test.com"})
    print(r.text)

register()