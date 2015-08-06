from Aaaah.base.primitives import *
from Aaaah.base.composites import *
from Aaaah.base.generators import *
from math import pi, sin, cos, sqrt

g = Group()
n = 60
largeur = 200
frac = 6*pi / n
for i in range(0,n):
	l = sin(frac*i+0.5) * 30
	g.add(line(1, 100+i*int(largeur/n), 100, 0, l))

m = Map()
m.add(g)
to_clipboard(m)