from assassins import Player, AssassinsGame

a = Player('miles', None)
b = Player('jess', None)
c = Player('chris', None)
g = AssassinsGame([a, b, c])
print g
g.disappear(a)
print g
g.disappear(b)
print g
print "And the winner is: {}".format(g.winner())
