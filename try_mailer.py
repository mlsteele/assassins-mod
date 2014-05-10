import time
import mailer

timestamp = time.strftime("%Y-%m-%d %I:%M %p", time.localtime())

outgoing_host = "smtp.mandrillapp.com"
from_addr = "assassins-master@mit.edu"
to_addr = "miles@milessteele.com"
subject = "Hey There"
body = "mailer test\n{}".format(timestamp)

mailer.send(outgoing_host, from_addr, to_addr, subject, body)
