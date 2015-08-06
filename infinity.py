from Aaaah.base.primitives import *
from Aaaah.base.composites import *
from Aaaah.base.generators import *
from math import cos, tan, sqrt, pi

"""
Inspired from http://tex.stackexchange.com/a/159086
"""

def frange(x, y, jump):
	while x < y:
		yield x
		x += jump

def getCenterRadius(t):
	a, b, h, k = 1, 1, 0, 0
	cX = a*(1/cos(t)) + h
	cY = b*tan(t) + k
	R = sqrt((cX-h)**2 + (cY-k)**2)
	return cX*30, cY*30, R

g = Group()
m = Map()
i = 0
for t in frange(-1.56, 1.56, 0.0284):
	xL,yL,RL = getCenterRadius(t)
	xR,yR,RR = getCenterRadius(pi+t)
	g.add(circle(1, Shape.Empty, 300+xL, 200+yL, RL*30))
	g.add(circle(1, Shape.Empty, 300+xR, 200+yR, RR*30))
	i = i + 1

#g.add(circle(1, Shape.Empty, 100, 100, 100))
#g.add(line(1, 0, 0, 100, 100))
m.add(g)
to_clipboard(m)
print(i*2, "circles")