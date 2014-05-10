import sys
import re
import os
import argparse
import time
import string
import smtplib
from datetime import datetime

time_str = time.strftime("%Y-%m-%d %I:%M %p", time.localtime())

msg = {
  "host": "outgoing.mit.edu",
  "subject": "$1 for hacks",
  "from": "-@mit.edu",
  "to": ["-@mit.edu"],
  "cc": "cash@square.com",
  "body": time_str + "\nMoney money money!",
}

msg_raw = string.join((
  "From: %s" % msg["from"],
  "To: %s" % ', '.join(msg["to"]),
  "Subject: %s" % msg["subject"] ,
  "Cc: %s" % msg["cc"] ,
  "",
  msg["body"]
  ), "\r\n")

server = smtplib.SMTP(msg["host"])
server.sendmail(msg["from"], msg["to"], msg_raw)
server.quit()
