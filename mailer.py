import smtplib
import collections
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

NEWLINE = "\r\n"


def send(outgoing_host, from_addr, to_addr, subject, body, cc_addr=None):
  """
  Send an email.
  outgoing_host is the outgoing host
  from_addr is the email addres to send from
  to_addr is the email addres or iterable of addresses to send to
  subject is the subject of the message
  body is the body of the message
  cc_addr is the email addres or iterable of addres to cc.
  """
  logger.info('Sending mail from {} to {}'.format(from_addr, to_addr))
  msg_raw = ""
  msg_raw += "From: {}".format(from_addr) + NEWLINE
  msg_raw += "To: {}".format(comma_sep(to_addr)) + NEWLINE
  msg_raw += "Subject: {}".format(subject) + NEWLINE
  if cc_addr != None:
    msg_raw += "CC: {}".format(comma_sep(cc)) + NEWLINE
  msg_raw += NEWLINE + body + NEWLINE

  logger.debug("Opening connection to {}".format(outgoing_host))
  server = smtplib.SMTP(outgoing_host)
  logger.debug("Sending message.")
  server.sendmail(from_addr, to_addr, msg_raw)
  logger.debug("Disconnecting from {}".format(outgoing_host))
  server.quit()


def comma_sep(string_or_list):
  """
  Format a string or iterable of strings into a comma separated list.
  For example:
    'a' -> 'a'
    ['a', 'b'] -> 'a, b'
  """
  if isinstance(string_or_list, basestring):
    return string_or_list
  else:
    return ', '.join(string_or_list)


# time_str = time.strftime("%Y-%m-%d %I:%M %p", time.localtime())
