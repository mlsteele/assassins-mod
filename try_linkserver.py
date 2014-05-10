from linkserver import LinkServer

def callback_generator(what_to_print):
  def callback():
    print what_to_print
  return callback

ls = LinkServer()
print "http://localhost:5000" + ls.register(callback_generator("some callback 1"))
print "http://localhost:5000" + ls.register(callback_generator("some callback 2"))
print "http://localhost:5000" + ls.register(callback_generator("only once!"), once=True)
ls.serve()
