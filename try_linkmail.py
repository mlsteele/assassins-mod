import time
import mailer
from linkserver import LinkServer

def thing_that_happens_once():
  print "\n\n\nThis happens, but only once.\n\n\n"

linkserver_host = "http://localhost:5000"
ls = LinkServer()
event_url = linkserver_host + ls.register(thing_that_happens_once, once=True)

outgoing_host = "outgoing.mit.edu"
from_addr = "assassins-master@mit.edu"
to_addr = "mlsteele@mit.edu"
subject = "Link Mail"
body = "Click this: {}".format(event_url)

mailer.send(outgoing_host, from_addr, to_addr, subject, body)

ls.serve()
