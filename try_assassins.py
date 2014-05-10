from assassins import Player, AssassinsGame

a = Player('miles', None)
b = Player('jess', None)
c = Player('chris', None)
g = AssassinsGame([a, b, c])
print "{} -> {}".format(a, g.target_of(a))
print "{} -> {}".format(b, g.target_of(b))
print "{} -> {}".format(c, g.target_of(c))
