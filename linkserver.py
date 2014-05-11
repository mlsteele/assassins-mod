"""
Server that listens for events over http and can call callbacks.
"""

from flask import Flask
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class LinkServer(object):
  def __init__(self):
    # mapping from event_id to (callback, once)
    self.callbacks = {}

  def register(self, callback, once=False):
    """
    Register a callback.
    Return the urlpath to fire the callback.
    """
    assert self._get_callback_id(callback) == None
    event_id = uuid2slug(str(uuid.uuid4()))
    logger.debug("Registered event {}".format(event_id))
    self.callbacks[event_id] = (callback, once)
    return "/event/{}".format(event_id)

  def cancel(self, callback):
    """Disable a callback forever."""
    event_id = self._get_callback_id(callback)
    logger.debug("Canceled event {}".format(event_id))
    if event_id != None:
      del self.callbacks[event_id]

  def _get_callback_id(self, callback):
    """Return the id of a callback or None if it is note registered"""
    for event_id, entry in self.callbacks.iteritems():
      cb, once = entry
      if cb == callback:
        return event_id

  def _execute(self, event_id):
    """
    Run a callback if there is one.
    Return whether something happened.
    """
    if event_id in self.callbacks:
      logger.debug("Executing event {}".format(event_id))
      (cb, once) = self.callbacks[event_id]
      cb()
      if once:
        self.cancel(cb)
      return True
    else:
      logger.debug("Executing NON-event {}".format(event_id))
      return False

  def serve(self):
    """
    Start serving.
    This is blocking.
    """
    logger.info("Serving.")
    app = Flask(__name__)

    @app.route("/")
    def hello():
      return "Hello. This is a link server."

    @app.route("/stats")
    def stats():
      return "No stats."

    @app.route("/event/<event_id>")
    def event(event_id):
      logger.info("Received event {}".format(event_id))
      happened = self._execute(event_id)
      if happened:
        return "Oooh! That just happened."
      else:
        return "I'm afraid that didn't happen, Dave."

    app.run()


def uuid2slug(uuidstring):
  # http://stackoverflow.com/questions/12270852/convert-uuid-32-character-hex-string-into-a-youtube-style-short-id-and-back
  return uuid.UUID(uuidstring).bytes.encode('base64').rstrip('=\n').replace('/', '_')
