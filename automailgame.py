from collections import defaultdict
import logging

import mailer
from linkserver import LinkServer
from assassins import Player, AssassinsGame

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

LINKSERVER_HOST = "http://7d4ceadf.ngrok.com"


class AutoMailGame(object):
  def __init__(self, players):
    self.players = players
    logger.info("Creating game.")
    logger.info("Players: {}".format(self.players))
    self._ls = LinkServer()
    # a list of callbacks that should be canceled when the game ends
    self._cancel_on_win = []
    # mapping from players to callbacks that should be canceled when they die
    self._cancel_on_death = defaultdict(lambda: [])
    self._game_over = False
    self._game_over_message_sent = False

  def start(self):
    self._invite_players()
    self._ls.serve()

  def _invite_players(self):
    """Invite all players."""
    logger.info("Inviting players.")
    self._waiting_for = list(self.players)
    for player in self._waiting_for:
      self._invite_player(player)

  def _invite_player(self, player):
    """Invite a player."""
    def on_player_join(player):
      logger.debug("Invitation accepted by: {}".format(player))
      self._waiting_for.remove(player)
      if len(self._waiting_for) == 0:
        self._start_game()

    logger.debug("Inviting player: {}".format(player))
    subject = "Would you like to play a game?"
    body = "Hey PLAYER_NAME,\nPlay assassins with us!\nTo join: EVENT_URL"
    cb = self._mail_player(player, subject, body, lambda: on_player_join(player))
    self._cancel_on_win.append(cb)

  def _start_game(self):
    logger.info("Starting game.")
    self._game = AssassinsGame(players)
    self._notify_tasks()

  def _notify_tasks(self):
    """Notify all players of their targets."""
    logger.info("Notifying all players of tasks.")
    for player in self._game.whos_alive():
      self._notify_task(player)

  def _notify_task(self, player):
    target = self._game.target_of(player)
    logger.debug("Notifying {} about their target {}".format(player, target))
    subject = "Assassins Target Assignment"
    body = "Your new target is {}\n\nOnce you've killed them: EVENT_URL".format(target.name)
    cb = self._mail_player(player, subject, body, lambda: self._on_kill(player, target))
    self._cancel_on_death[player].append(cb)
    self._cancel_on_win.append(cb)

  def _on_kill(self, player, target):
    """
    Called when a player reports a kill.
    (Could be called when game is already won.)
    """
    logger.info("Kill made by {} of {}".format(player, target))
    if not self._game_over:
      # cancel target actions
      for cb in self._cancel_on_death[target]:
        self._ls.cancel(cb)
      self._game.disappear(target)
      self._check_for_win()
    else:
      self._on_win()

  def _check_for_win(self):
    """Check for a win condition and activate."""
    if self._game.winner() != None:
      self._on_win()

  def _on_win(self):
    """
    Called whenever someone has won.
    (Could be called multiple times)
    """
    assert self._game.winner() != None

    # cancel old callbacks
    for cb in self._cancel_on_win:
      self._ls.cancel(cb)

    logger.info("Game over.")
    logger.info("Winner: {}".format(self._game.winner()))

    if not self._game_over_message_sent:
      for player in self.players:
        logger.debug("Notifying {} about GAME OVER".format(player))
        subject = "Assassins Game Over"
        body = "It's over.\n{} won!".format(self._game.winner().name)
        self._mail_player(player, subject, body)

      self._game_over_message_sent = True


  def _mail_player(self, player, subject, body, then=None):
    """
    Mail a player.
    Use 'then' as a callback and register an event url.
    Replaces 'EVENT_URL' in the body with the event url.
    Replaces 'PLAYER_NAME' in the body with the player's name.
    Returns the 'then' callback if there is one.
    """
    logger.debug("Mailing {}".format(player))
    if then != None:
      event_url = LINKSERVER_HOST + self._ls.register(then, once=True)
      body = body.replace("EVENT_URL", event_url)
    body = body.replace("PLAYER_NAME", player.name)
    mailer.send("outgoing.mit.edu", "assassins-master@mit.edu", player.email, subject, body)
    return then


if __name__ == "__main__":
  players = []
  players.append(Player('Miles1', 'miles@milessteele.com'))
  players.append(Player('Miles2', 'mlsteele@mit.edu'))

  amg = AutoMailGame(players)
  amg.start()
