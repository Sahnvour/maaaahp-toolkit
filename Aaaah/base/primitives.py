from operator import attrgetter
import xml.etree.ElementTree as ET
from . import pyperclip


def to_clipboard(anything):
	pyperclip.copy(str(anything))



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


	def __init__(self, X, Y, start=-1000, duration=1001, loop=Transform.NoLoop):
		if isinstance(loop, int):
			loop = str(loop)
		Transform.__init__(self, Transform.Translation, start, duration, loop)
		self.X = X
		self.Y = Y

	def params(self):
		p = "P=\"{0},{1},{2},{3},{4}\""
		return p.format(self.start, self.duration, self.X, self.Y, self.loop)



class Rotation(Transform):


	def __init__(self, angle, start=-1000, duration=1001, loop=Transform.NoLoop):
		if angle == 0:
			self.isIdentity = True
		else:
			if isinstance(loop, int):
				loop = str(loop)
			Transform.__init__(self, Transform.Rotation, start, duration, loop)
			self.angle = angle

	def params(self):
		p = "P=\"{0},{1},{2},{3}\""
		return p.format(self.start, self.duration, self.angle, self.loop)



class _Transformable():


	def __init__(self):
		self.rotation = None
		self.translation = None

	def rotate(self, *args):
		if len(args) == 1 and isinstance(args[0], Rotation):
			self.rotation = rotation
		elif len(args) == 4:
			self.rotation = Rotation(*args)
		else:
			raise ValueError(" incorrect arguments provided to Shape.rotate()")

	def translate(self, *args):
		if len(args) == 1 and isinstance(args[0], Translation):
			self.translation = translation
		elif len(args) == 5:
			self.translation = Translation(*args)
		else:
			raise ValueError(" incorrect arguments provided to Shape.translate()")



class Group(_Transformable):


	def __init__(self, *args):
		_Transformable.__init__(self)
		self.shapes = []
		self.add(*args)
		self.setup()

	def __str__(self):
		g = "<G P=\"{0},{1}\">".format(self.X, self.Y)
		g += ''.join(map(str, self.shapes)) + "</G>"
		return g

	def __len__(self):
		return len(self.shapes)

	def setup(self):
		if len(self.shapes):
			self.X = max(self.shapes, key=attrgetter("X")).X
			self.Y = max(self.shapes, key=attrgetter("Y")).Y

	def add(self, *shapes):
		for s in shapes:
			if isinstance(s, Group):
				for s1 in s.shapes:
					self.shapes.append(s1)
			else:
				s.rotate(Transform.Identity)
				s.translate(Transform.Identity)
				self.shapes.append(s)
			s.group = self
		self.setup()

	def remove(self, shape):
		if shape in self.shapes:
			self.shapes.remove(shape)
			shape.group = None

	def rotate(self, rotation):
		Transform.rotate(self, rotation)
		self.shapes[0].rotate(rotation)

	def translate(self, translation):
		Transform.translate(self, translation)
		self.shapes[0].translate(translation)



class Shape(_Transformable):


	Full = True
	Empty = False

	def __init__(self, letter, thickness, X, Y, width, height):
		_Transformable.__init__(self)
		self.group = None
		self.letter = letter
		self.thickness = thickness
		self.X = X
		self.Y = Y
		self.L = width
		self.H = height
		self.rotation = Transform.Identity
		self.translation = Transform.Identity

	def params(self):
		p = "P=\"{0},{1},{2},{3},{4}\""
		return p.format(self.thickness, self.X, self.Y, self.L, self.H)

	def __str__(self):
		if self.rotation.isIdentity and self.translation.isIdentity:
			return "<{0} {1}/>".format(self.letter, self.params())
		else:
			p = "<{0} {1}>{2}{3}</{0}>"
			return p.format(self.letter, self.params(), self.rotation, self.translation)
		


class _Curve(Shape):


	def __init__(self, thickness, X1, Y1, pivotX, pivotY, X2, Y2):

		self.pivotX = pivotX
		self.pivotY = pivotY
		Shape.__init__(self, "C", thickness, X1, Y1, X2, Y2)

	def params(self):
		p = "P=\"{0},{1},{2},{3},{4},{5},{6}\""
		return p.format(self.thickness, self.X, self.Y, self.pivotX, self.pivotY, self.L, self.H)



class _FullOrEmptyShape(Shape):
	
	
	Rectangle = 'R'
	Ellipse = 'E'

	def __init__(self, letter, thickness, isFull, X, Y, width, height):
		self.isFull = isFull
		Shape.__init__(self, letter, thickness, X, Y, width, height)

	def params(self):
		p = "P=\"{0},{1},{2},{3},{4},{5}\""
		return p.format(self.thickness, self.X, self.Y, self.L, self.H, 1 if self.isFull else 0)



def line(thickness, X1, Y1, width, height):
	return Shape("L", thickness, X1, Y1, width, height)

def rectangle(thickness, isFull, X, Y, width, height):
	return _FullOrEmptyShape(_FullOrEmptyShape.Rectangle, thickness, isFull, X, Y, width, height)

def ellipse(thickness, isFull, X, Y, width, height):
	return _FullOrEmptyShape(_FullOrEmptyShape.Ellipse, thickness, isFull, X, Y, width, height)

def curve(thickness, X1, Y1, pivotX, pivotY, X2, Y2):
	return _Curve(thickness, X1, Y1, pivotX, pivotY, X2, Y2)

SHAPE_TAGS = {
		'L' : line,
		'R' : rectangle,
		'E' : ellipse,
		'C' : curve
	}

def make_shape(tag, *args):
	return SHAPE_TAGS[tag](*args)


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

	def __len__(self):
		return len(self.shapes) + sum(map(len, self.groups))

	def add(self, *shapes):
		for s in shapes:
			if isinstance(s, Group):
				self.groups.append(s)
			else:
				self.shapes.append(s)

	def remove(self, shape):
		if isinstance(shape, Group):
			self.groups.remove(shape)
		else:
			self.shapes.remove(shape)

	def to_file(self, filename):
		with open(filename, "w") as save_file:
			save_file.write(str(self).encode('utf8'))

	make_shape = {
		'L' : line,
		'R' : rectangle,
		'E' : ellipse,
		'C' : curve
	}

	@staticmethod
	def _make_shape(elem):
		args = elem.get('P').split(',')
		args = list(map(int, args))

		if elem.tag in "RE": # fullness is arg #5 in map code
			args = [args[i] for i in [0, 5, 1, 2, 3, 4]] # fix arg order

		shape = make_shape(elem.tag, *args)

		for tr_rot in elem: # handle translations and rotations
			targs = tr_rot.get('P').split(',')
			targs = list(map(int, targs))

			if tr_rot.tag == 'R': # rotation
				targs = [targs[i] for i in [2, 0, 1, 3]] # fix arg order
				shape.rotate(*targs)

			elif tr_rot.tag == 'T': # translation
				targs = [targs[i] for i in [2, 3, 0, 1, 4]] #fix arg order
				shape.translate(*targs)

		return shape

	@staticmethod
	def _build(func, source):
		m = Map()
		tree = func(source)
		root = tree.getroot()

		free_shapes = root.find('F')	# tous les enfants de la balise <F>
		for s in free_shapes:			# à savoir les formes libres
			shape = Map._make_shape(s)
			m.add(shape)

		return m

	@staticmethod
	def from_file(filename):
		return Map._build(ET.parse, filename)

	@staticmethod
	def from_str(data):
		return Map._build(ET.fromstring, data)
