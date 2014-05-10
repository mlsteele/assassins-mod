import time
import mailer

timestamp = time.strftime("%Y-%m-%d %I:%M %p", time.localtime())

outgoing_host = "outgoing.mit.edu"
from_addr = "mlsteele@mit.edu"
to_addr = "miles@milessteele.com"
subject = "Hey There"
body = "mailer test\n{}".format(timestamp)

mailer.send(outgoing_host, from_addr, to_addr, subject, body)
