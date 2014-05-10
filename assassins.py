"""
In-memory implementation of game logic.
"""

import random
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Player(object):
  def __init__(self, name, email):
    logger.debug("Creating player {}".format(name))
    self.name = name
    self.email = email

  def __repr__(self):
    return "<Player name:{} email:{}>".format(self.name, self.email)


class AssassinsGame(object):
  def __init__(self, players):
    logger.info("Creating AssassinsGame")
    self.players = players

    # mapping from player to whether they're alive.
    self.alive = {p: True for p in self.players}

    # assign targets
    self.targets = {}
    randomized_list = shuffled(self.players)
    for a, b in zip(randomized_list, rotated(randomized_list)):
      self.targets[a] = b

  def disappear(self, target):
    logger.info("Disappearing {}".format(target.name))
    assert target in self.players
    assert target in self.whos_alive()
    # kill target
    self.alive[target] = False

    # update targets
    for p in self.players:
      if self.targets[p] == target:
        self.targets[p] = self.targets[target]
    self.targets[target] = None

  def whos_alive(self):
    return [p for p in self.alive if self.alive[p]]

  def target_of(self, player):
    assert player in self.players
    assert player in self.whos_alive()
    return self.targets[player]

  def winner(self):
    """
    Get the winner of the game.
    returns None until there is a winner.
    """
    if len(self.whos_alive()) == 1:
      return self.whos_alive()[0]
    else:
      return None

  def __str__(self):
    header = "<AssassinsGame with {}/{} players>".format(len(self.whos_alive()), len(self.players))
    tasks = ["  {} -> {}".format(p, self.target_of(p)) for p in self.whos_alive()]
    return '\n'.join([header] + tasks)


def rotated(l):
  return l[1:] + [l[0]]

def shuffled(l):
  l2 = list(l)
  random.shuffle(l2)
  return l2
