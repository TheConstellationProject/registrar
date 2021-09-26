#!/usr/bin/python3
import json
import datetime
import sys

try:
    x = sys.argv[1]
    y = sys.argv[2]
except IndexError:
    print("Usage: ./update.py 'Name of article' 'link'")
    exit(1)

_ = {}

with open("updates.json", 'r') as x:
    _ = json.load(x)

_[str(sys.argv[1])] =  {
                    "date": datetime.datetime.now().strftime("%B %-d, %Y"),
                    "link": str(sys.argv[2])
                    }


with open("updates.json", 'w') as x:
    x.write(json.dumps(_))
