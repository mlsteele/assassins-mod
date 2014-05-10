import time
import mailer
import logging
from linkserver import LinkServer
from assassins import Player, AssassinsGame

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def mail_player(player, subject, body):
  mailer.send("outgoing.mit.edu", "assassins-master@mit.edu", player.email, subject, body)

LINKSERVER_HOST = "http://64444de.ngrok.com"

ls = LinkServer()

def invite_players(players, then):
  """
  Invite playres to a game.
  then is a callback to run once everyone has joined.
  """
  logger.info("Inviting all players")
  waiting_for_players = list(players)

  def on_player_join(player):
    logger.info("Accepted invitation {}".format(player))
    waiting_for_players.remove(player)
    if len(waiting_for_players) == 0:
      then()

  def invite_player(player):
    logger.info("Inviting {}".format(player))
    url_player_join = LINKSERVER_HOST + ls.register(lambda: on_player_join(player), once=True)
    subject = "Would you like to play a game?"
    body = "Play assassins with us!\nTo join: {}".format(url_player_join)
    mail_player(player, subject, body)

  # send invitations
  for player in waiting_for_players:
    invite_player(player)

def notify_task(player, target, on_complete):
  """
  Notify a player about a new target
  on_complete is a callback to run when that player completes the task.
  """
  logger.info("Notifying {} about their target {}".format(player, target))
  url_player_join = LINKSERVER_HOST + ls.register(on_complete, once=True)
  subject = "Assassins Target Assignment"
  body = "Your new target is {}\n\nOnce you've killed them: {}".format(target.name, url_player_join)
  mail_player(player, subject, body)

def start_game(players):
  logger.info("Starting game")
  game = AssassinsGame(players)

  def outer_notify_task(player):
    target = game.target_of(player)
    def on_complete():
      logger.info("Completed task by {}".format(player))
      if game.winner() != None:
        game.disappear(target)
      else:
        ls.cancel(on_complete)
        # TODO game has winner
    notify_task(player, target, on_complete)

  for player in game.whos_alive():
    outer_notify_task(player)


def print_good_things():
  print "Good things."

players = []
players.append(Player('Miles1', 'miles@milessteele.com'))
players.append(Player('Miles2', 'mlsteele@mit.edu'))

invite_players(players, lambda: start_game(players))

# start listening
ls.serve()
