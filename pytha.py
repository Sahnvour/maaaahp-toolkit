from Aaaah.primitives import *
from Aaaah.composites import *

def pythagoreasTree(shapes, x, y, w, h, offset, higherDiag, step, n):
	if(step > n):
		return

	x0, y0, x1, y1 = x, y, w, h

	x2 = -y0 + x1 + y1
	y2 = x0 - x1 + y1
	x3 =  y1 + x0 - y0
	y3 = -x1 + x0 + y0

	full = Shape.Empty if step == n else Shape.Full

	if step > 0:
		rect = AnyRectangle(1, x0, y0-400, x1, y1-400, x2, y2-400, x3, y3-400, full)
		diag = rect.L/sqrt(2) # triangle rectangle isocele
		#dist = offset - diag
		rect.translate(Translation(rect.X, rect.Y+400 + offset, step*4, 2))
		rect.rotate(Rotation(45*step % 90, step*4+2, 1))
	else:
		rect = AnyRectangle(1, x0, y0, x1, y1, x2, y2, x3, y3, Shape.Full)
		diag = rect.L/sqrt(2) # triangle rectangle isocele
	shapes.append(rect)

	x4 = x3 + (x2-x0)*0.5
	y4 = y3 + (y2-y0)*0.5

	if step == 0:
		offset = diag + (diag - rect.L)
	else:
		offset = offset + higherDiag - diag
	pythagoreasTree(shapes, x3, y3, x4, y4, offset, diag, step+1, n)
	pythagoreasTree(shapes, x4, y4, x2, y2, offset, diag, step+1, n)

m = Map()
p = []
pythagoreasTree(p, 350, 305, 425, 305, 0, 0, 0, 6)
for s in p:
	m.add(s)
m.add(Rectangle(1, 0, 380, 800, 20, Shape.Full))
m.toFile("pythagoreastree2.txt")
toClipBoard(m)