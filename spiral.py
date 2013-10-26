from Aaaah.base.primitives import *
from Aaaah.base.composites import *
from Aaaah.base.generators import *
from math import sin, cos, radians

def spiral(a, step, n, scale=1):
	angle, i = 0, 0
	m = Map()
	g = Group()

	while i < n:
		angle = i * step
		x = a * angle * cos(radians(angle))
		y = a * angle * sin(radians(angle))
		x = x * scale
		y = y * scale
		sphere = ellipsis(1, x+400, y+200, 1, 1, Shape.Full if i%2 else Shape.Empty)
		g.add(sphere)
		i = i + 1

	m.add(g)
	to_clipboard(m)

def squares(x, y, width, height, n):

	m = Map()
	g = Group()
	x, y =
	for i in range(n):


spiral(1.6, 10, 120, 0.12)