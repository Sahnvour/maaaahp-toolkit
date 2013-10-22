from .primitives import *
from math import sin, cos, radians, degrees, atan2, sqrt

def grey_line(X, Y, lenght, vertical=False):
	if vertical:
		return Curve(1, X, Y, 0, lenght * 2, 0, 0)
	else:
		return Curve(1, X, Y, lenght * 2, 0, 0, 0)	


def grey_block(X, Y, width, height):
	g = Group()

	if width > height:
		for i in range(0, height/2):
			g.add(grey_line(X, Y + i * 2, width))
	else:
		for i in range(0, width/2):
			g.add(grey_line(X + i * 2, Y, height, True))

	return g


def triangle(thickness, x1, y1, x2, y2, x3, y3):
	l1 = line(thickness, x1, y1, x2 - x1, y2- y1)
	l2 = line(thickness, x2, y2, x3 - x2, y3 - y2)
	l3 = line(thickness, x1, y1, x3 - x1, y3 - y1)
	return Group(l1, l2, l3)


def angle(thickness, x, y, lenght1, lenght2, angle, angleToOrigin=0):
	angle = radians(angle)
	angle2 = radians(angleToOrigin-90)

	x1 = lenght1 * cos(angle2)
	y1 = lenght1 * sin(angle2)
	line1 = line(thickness, x, y, x1, y1)

	x1 = lenght2 * cos(angle2 + angle)
	y1 = lenght2 * sin(angle2 + angle)
	line2 = line(thickness, x, y, x1, y1)

	return Group(line1, line2)

def any_rectangle(thickness, x1, y1, x2, y2, x3, y3, x4, y4, isFull):
	width = sqrt( (x1-x2)**2 + (y1-y2)**2 )
	height = sqrt( (x2-x3)**2 + (y2-y3)**2 )

	deltaX, deltaY = x2-x1, y1-y2
	angle = -degrees(atan2(deltaY, deltaX))

	#rotation point at the center of the shape
	Ox = (x1 + x3) / 2
	Oy = (y1 + y3) / 2

	newx = (x1 - Ox) * cos(radians(-angle)) - (y1 - Oy) * sin(radians(-angle)) + Ox
	newy = (x1 - Ox) * sin(radians(-angle)) + (y1 - Oy) * cos(radians(-angle)) + Oy

	r = rectangle(thickness, newx, newy, width, height, isFull)
	r.rotate(Rotation(angle))

	return r