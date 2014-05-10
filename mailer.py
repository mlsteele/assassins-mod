import smtplib
import collections

NEWLINE = "\r\n"


def send(outgoing_host, from_addr, to_addr, body, cc_addr=None):
  """
  Send an email.
  outgoing_host is the outgoing host
  from_addr is the email addres to send from
  to_addr is the email addres or iterable of addresses to send to
  body is
  cc_addr is the email addres or iterable of addres to cc.
  """
  msg_raw = ""
  msg_raw += "From: {}".format(from_addr) + NEWLINE
  msg_raw += "To: {}".format(comma_sep(to_addr)) + NEWLINE
  msg_raw += "Subject: {}".format(subject) + NEWLINE
  if cc_addr != None:
    msg_raw += "CC: {}".format(comma_sep(cc)) + NEWLINE
  msg_raw += NEWLINE + body + NEWLINE

  server = smtplib.SMTP(outgoing_host)
  server.sendmail(from_addr, to_addr, msg_raw)
  server.quit()


def comma_sep(string_or_list):
  """
  Format a string or iterable of strings into a comma separated list.
  For example:
    'a' -> 'a'
    ['a', 'b'] -> 'a, b'
  """
  if isinstance(string_or_list, collections.Iterable):
    return ', '.join(string_or_list)
  else:
    return string_or_list


# time_str = time.strftime("%Y-%m-%d %I:%M %p", time.localtime())
