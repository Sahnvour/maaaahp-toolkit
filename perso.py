from Aaaah.base.primitives import *
from Aaaah.base.composites import *
from Aaaah.base.generators import *

def cordes():
	m = Map()
	
	nbCordes = 15
	lenght = 610/nbCordes
	height = (273-48)/nbCordes
	g = Group()
	for i in range(1,nbCordes+1):
		l = line(6, 70 + i*lenght, 270 - i*height, 0, 80)
		r = Rotation(360, Transform.Loop, 1, 2)
		l.rotate(r)
		g.add(l)

	m.add(g)
	m.add(rectangle(6, 100, 100, 100, 100, Shape.Full))
	m.add(ellipsis(6, 300, 300, 100, 100, Shape.Empty))
	m.to_file("maptest.txt")

def circleOfLines(carte, n, x, y, lenght, loop, thickness, start):
	nbCordes = n

	for i in range(0, nbCordes):
		line = line(thickness, x, y, 0, lenght)
		istart = start + i
		r = Rotation(360, loop, istart, istart + 1)
		line.rotate(r)
		carte.add(line)

def syphons():
	m = Map()

	m.add(rectangle(6, 0, 380, 802, 22, Shape.Full))

	circleOfLines(m, n=25, x=100, y=100, lenght=16, thickness=1, loop=Transform.LoopBack, start=2)
	circleOfLines(m, n=25, x=300, y=250, lenght=20, thickness=1, loop=Transform.LoopBack, start=2)
	circleOfLines(m, n=25, x=550, y=200, lenght=24, thickness=1, loop=Transform.LoopBack, start=2)
	circleOfLines(m, n=25, x=400, y=70, lenght=12, thickness=1, loop=Transform.LoopBack, start=2)

	m.to_file("maptest.txt")

def greyLadder(n, x, y, lenght):
	g = Group()

	for i in range(0,n-1):
		g.add(GreyLine(x, y+i*3, lenght))
	return g

"""
def pythagoreasTree(n, startSize):
	shapes = []
	rect = rectangle(6, 362.5, 250, startSize, startSize, Shape.Full)
	rect.rotate(Rotation(0))
	shapes.append(rect)
	print("Step %d size = %f" % (n, startSize))
	expand(rect, n-1, shapes, rect.X, rect.Y)

	return shapes

def expand(rect, n, shapes, centerX, centerY):
	print("Step " + str(n))
	if n == 0:
		return

	size = int(rect.L / sqrt(2))
	angle = rect.rotation.angle + 45
	x = (rect.X - size/2)
	y = (rect.Y - rect.L)
	X = centerX + (x-centerX)*cos(radians(45)) - (y-centerY)*sin(-radians(45))
	Y = centerY + (x-centerX)*sin(-radians(45)) + (y-centerY)*cos(radians(45))

	X1 = centerX + (X-centerX)*cos(radians(angle)) - (Y-centerY)*sin(-radians(angle))
	Y1 = centerY + (X-centerX)*sin(-radians(angle)) + (Y-centerY)*cos(radians(angle))

	X = X + rect.L
	Y = (rect.Y - rect.L)

	X2 = centerX + (X-centerX)*cos(radians(-angle)) - (Y-centerY)*sin(-radians(-angle))
	Y2 = centerY + (X-centerX)*sin(-radians(-angle)) + (Y-centerY)*cos(radians(-angle))

	r = Rotation(angle, 1, 1)
	t = Translation(rect.X-size, rect.Y-size, 1, 1)

	print("X1={0}  Y1={1}".format(X1, Y1))
	rect1 = rectangle(1, X1, Y1, size, size, Shape.Full)
	rect2 = rectangle(1, X2, Y2, size, size, Shape.Full)
	rect1.rotate(r)
	rect2.rotate(r)
	#rect1.translate(t)
	#rect2.translate(t)
	shapes.append(rect1)
	shapes.append(rect2)

	expand(rect1, n-1, shapes, X1, Y1)
	expand(rect2, n-1, shapes, X2, Y2)
"""

def testGen():
	m = Map()
	for l in row(line, 0, 0, 20)[0:25]:
		shape = l(1, 100, 100)
		shape.translate(Translation(300, 300))
		m.add(shape)
	to_clipboard(m)


if __name__ == "__main__":
	
	#testGen()
	
	m= Map()
	i = 0
	for k in Orientations.keys():
		m.add(half_circle(50, 70*(i+1), 200, k))
		i = i + 1
	to_clipboard(m)