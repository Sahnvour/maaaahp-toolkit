from operator import attrgetter
from . import pyperclip


def toClipBoard(anything):
	pyperclip.copy(str(anything))

class Vec2():
	def __init__(self, x, y):
		self.x = x
		self.y = y

Point = Vec2

class Map():

	def __init__(self):
		self.shapes = []
		self.groups = []

	def __str__(self):
		txt = "<C>"
		if self.groups:
			txt += "<G>" + ''.join(map(str, self.groups)) + "</G>"
		else:
			txt += "<G/>"

		if self.shapes:
			txt += "<F>" + ''.join(map(str, self.shapes)) + "</F></C>"
		else:
			txt += "<F/></C>"
		
		return txt

	def add(self, *shapeOrGroup):
		for s in shapeOrGroup:
			if s.isGroup:
				self.groups.append(s)
			else:
				self.shapes.append(s)

	def toFile(self, fileName):
		fichier = open(fileName, "w")
		fichier.write(str(self))
		fichier.close()


class Transform():

	NoLoop = '0'
	Loop = '1'
	LoopBack = '2'
	Translation = 'T'
	Rotation = 'R'
	
	def __init__(self, letter, start, duration, loop):
		self.isIdentity = False
		self.letter = letter
		self.start = start
		self.duration = duration
		self.loop = loop

	def __str__(self):
		if self.isIdentity:
			return ""
		else:
			return "<{0} {1}/>".format(self.letter, self.params())

Transform.Identity = Transform(None, None, None, None)
Transform.Identity.isIdentity = True


class Translation(Transform):

	def __init__(self, X, Y, start=-1000, duration=1, loop=Transform.NoLoop):
		Transform.__init__(self, Transform.Translation, start, duration, loop)
		self.X = X
		self.Y = Y

	def params(self):
		return "P=\"{0},{1},{2},{3},{4}\"".format(self.start, self.duration, self.X, self.Y, self.loop)


class Rotation(Transform):

	def __init__(self, angle, start=-1000, duration=1001, loop=Transform.NoLoop):
		if angle == 0:
			self.isIdentity = True
		else:
			Transform.__init__(self, Transform.Rotation, start, duration, loop)
			self.angle = angle

	def params(self):
		return "P=\"{0},{1},{2},{3}\"".format(self.start, self.duration, self.angle, self.loop)


class _Transformable():

	def __init__(self):
		self.rotation = None
		self.translation = None

	def rotate(self, rotation):
		self.rotation = rotation

	def translate(self, translation):
		self.translation = translation


class Group(_Transformable):

	def __init__(self, *args):
		_Transformable.__init__(self)
		self.isGroup = True
		self.shapes = []
		for s in args:
			s.rotate(Transform.Identity)
			s.translate(Transform.Identity)
			self.shapes.append(s)
		self.setup()

	def __str__(self):
		return "<G P=\"{0},{1}\">".format(self.X, self.Y) + ''.join(map(str, self.shapes)) + "</G>"

	def setup(self):
		if len(self.shapes):
			self.X = max(self.shapes, key=attrgetter("X")).X
			self.Y = max(self.shapes, key=attrgetter("Y")).Y

	def add(self, *shapes):
		for s in shapes:
			if s.isGroup:
				for s1 in s.shapes:
					self.shapes.append(s1)
			else:
				s.rotate(Transform.Identity)
				s.translate(Transform.Identity)
				self.shapes.append(s)
		self.setup()

	def rotate(self, rotation):
		Transform.rotate(self, rotation)
		self.shapes[0].rotate(rotation)

	def translate(self, translation):
		Transform.translate(self, translation)
		self.shapes[0].translate(translation)


class Shape(_Transformable):

	Full = True
	Empty = False

	def __init__(self, letter, thickness, X, Y, lenght, height):
		_Transformable.__init__(self)
		self.isGroup = False
		self.letter = letter
		self.thickness = thickness
		self.X = X
		self.Y = Y
		self.L = lenght
		self.H = height
		self.rotation = Transform.Identity
		self.translation = Transform.Identity

	def params(self):
		return "P=\"{0},{1},{2},{3},{4}\"".format(self.thickness, self.X, self.Y, self.L, self.H)

	def __str__(self):
		if self.rotation.isIdentity and self.translation.isIdentity:
			return "<{0} {1}/>".format(self.letter, self.params())
		else:
			return "<{0} {1}>{2}{3}</{0}>".format(self.letter, self.params(), self.rotation, self.translation)
		

class Curve(Shape):

	def __init__(self, thickness, X1, Y1, pivotX, pivotY, X2, Y2):

		self.pivotX = pivotX
		self.pivotY = pivotY
		Shape.__init__(self, "C", thickness, X1, Y1, X2, Y2)

	def params(self):
		return "P=\"{0},{1},{2},{3},{4},{5},{6}\"".format(self.thickness, self.X, self.Y, self.pivotX, self.pivotY, self.L, self.H)


class _FullOrEmptyShape(Shape):
	
	Rectangle = 'R'
	Ellipsis = 'E'

	def __init__(self, letter, thickness, X, Y, lenght, height,isFull):
		self.isFull = isFull
		Shape.__init__(self, letter, thickness, X, Y, lenght, height)

	def params(self):
		return "P=\"{0},{1},{2},{3},{4},{5}\"".format(self.thickness, self.X, self.Y, self.L, self.H, 1 if self.isFull else 0)


def Line(thickness, X1, Y1, X2, Y2):
	return Shape("L", thickness, X1, Y1, X2, Y2)


def Rectangle(thickness, X, Y, lenght, height, isFull):
	return _FullOrEmptyShape(_FullOrEmptyShape.Rectangle, thickness, X, Y, lenght, height, isFull)


def Ellipsis(thickness, X, Y, lenght, height, isFull):
	return _FullOrEmptyShape(_FullOrEmptyShape.Ellipsis, thickness, X, Y, lenght, height, isFull)
