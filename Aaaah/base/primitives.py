from operator import attrgetter
import xml.etree.ElementTree as ET
from . import pyperclip


def to_clipboard(anything):
	"""
	Copy the string of anything into user's clipboard.

	"""
	pyperclip.copy(str(anything))



class Transform():
	"""
	A transform base class.

	"""

	NoLoop = '0'
	Loop = '1'
	LoopBack = '2'
	Translation = 'T'
	Rotation = 'R'
	Identity = None
	
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



class Translation(Transform):
	"""
	A translation class.

	"""

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
	"""
	A rotation class.

	"""

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
		"""
		Rotate a transformable (shape or group) by providing a Rotation object
		or arguments to instanciate one.
		
		>>> r = rectangle(5,Shape.Empty,100,100,50,50)
		>>> myrot = Rotation(360, 0, 10, Transform.Loop)
		>>> r.rotate(myrot)
		>>> another_rect.rotate(myrot)
		>>> some_line.rotate(180, 0, 2, Transform.LoopBack)

		"""
		if len(args) == 1:
			if isinstance(args[0], Rotation):
				self.rotation = args[0]
			elif args[0] == None:
				self.rotation = None

		elif len(args) == 4:
			self.rotation = Rotation(*args)
		else:
			raise ValueError(" incorrect arguments provided to Shape.rotate()")

	def translate(self, *args):
		"""
		Translate a transformable (shape or group) by providing a Translation
		object or arguments to instanciate one.
		
		>>> r = rectangle(5,Shape.Empty,100,100,50,50)
		>>> my_translate = Translation(200, 200, 0, 10, Transform.LoopBack)
		>>> r.translate(my_translate)
		>>> another_rect.translate(my_translate)
		>>> some_line.translate(0, 0, 0, 2, Transform.NoLoop)

		"""
		if len(args) == 1:
			if isinstance(args[0], Translation):
				self.translation = args[0]
			elif args[0] == None:
				self.translation = None

		elif len(args) == 5:
			self.translation = Translation(*args)
		else:
			raise ValueError(" incorrect arguments provided to Shape.translate()")



class Group(_Transformable):
	"""
	A class representing a group of shapes.
	
	Shapes can be added and removed from a group.
	One can apply rotations and translations to a group, hence applying
	these transforms to all the shapes in the group.

	"""

	def __init__(self, *args):
		_Transformable.__init__(self)
		self.shapes = []
		self.add(*args)
		self._setup()

	def __str__(self):
		g = "<G P=\"{0},{1}\">".format(self.X, self.Y)
		g += ''.join(map(str, self.shapes)) + "</G>"
		return g

	def __len__(self):
		return len(self.shapes)

	def _setup(self):
		if len(self.shapes):
			self.X = max(self.shapes, key=attrgetter("X")).X
			self.Y = max(self.shapes, key=attrgetter("Y")).Y

	def add(self, *shapes):
		"""
		Add some shapes or another group to a group.

		>>> g = Group()
		>>> g.add(line(1,0,0,100,100))
		>>> g.add(mycurve, mygroup, myrectangle)

		Adding a group to an other will transfer all the shapes of the second
		one into the first one.

		"""
		for s in shapes:
			if isinstance(s, Group):
				self.shapes.extend(s.shapes)
				s.shapes.clear()
			else:
				s.rotate(Transform.Identity)
				s.translate(Transform.Identity)
				self.shapes.append(s)
			s.group = self
		self._setup()

	def remove(self, shape):
		"""
		Remove a shape reference from a group.

		>>> g = Group()
		>>> l = line(1,0,0,100,100)
		>>> g.add(l)
		>>> len(g)
		1
		>>> g.remove(l)
		>>> len(g)
		0

		"""
		if shape in self.shapes:
			self.shapes.remove(shape)
			shape.group = None
		self._setup()

	def rotate(self, *args):
		"""
		Rotate a group by providing a Rotation object or arguments to
		instanciate one.

		Note that this will affect the rotation to the first shape of the group.
		
		>>> g = Group()
		>>> g.add(shape1, shape2)
		>>> rot = Rotation(360, 0, 10, Transform.Loop)
		>>> g.rotate(rot)
		>>> g.rotate(180, 0, 2, Transform.LoopBack)

		"""
		_Transformable.rotate(self, *args)
		self.shapes[0].rotate(*args)

	def translate(self, *args):
		"""
		Translate a group by providing a Translation object or arguments to
		instanciate one.
		
		>>> g = Group()
		>>> g.add(shape1, shape2)
		>>> trans = Translation(400, 200, 0, 10, Transform.Loop)
		>>> g.translate(trans)
		>>> g.translate(200, 100, 0, 2, Transform.NoLoop)

		"""
		_Transformable.translate(self, *args)
		self.shapes[0].translate(*args)



class Shape(_Transformable):
	"""
	Base class for the primitive shapes.

	It should not be instanciated as-is, instead always use the primitive
	functions line, curve, ellipse and rectangle.

	"""

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
		if self.rotation is Transform.Identity \
		and self.translation is Transform.Identity:

			return "<{0} {1}/>".format(self.letter, self.params())
		else:
			s = "<{0} {1}>{2}{3}</{0}>"
			return s.format(self.letter, self.params(), \
							self.rotation if self.rotation else '', \
							self.translation if self.translation else '')
		


class _Curve(Shape):


	def __init__(self, thickness, X1, Y1, pivotX, pivotY, X2, Y2):

		self.pivotX = pivotX
		self.pivotY = pivotY
		Shape.__init__(self, "C", thickness, X1, Y1, X2, Y2)

	def params(self):
		p = "P=\"{0},{1},{2},{3},{4},{5},{6}\""
		return p.format(self.thickness, self.X, self.Y, self.pivotX, \
						self.pivotY, self.L, self.H)



class _FullOrEmptyShape(Shape):
	
	
	Rectangle = 'R'
	Ellipse = 'E'

	def __init__(self, letter, thickness, isFull, X, Y, width, height):
		self.isFull = isFull
		Shape.__init__(self, letter, thickness, X, Y, width, height)

	def params(self):
		p = "P=\"{0},{1},{2},{3},{4},{5}\""
		return p.format(self.thickness, self.X, self.Y, self.L, self.H, \
						1 if self.isFull else 0)



def line(thickness, X1, Y1, width, height):
	"""
	Return a line shape.

	Creating a line from point (50, 100) to (250, 400) of thickness 5:

	>>> line(5, 50, 100, 200, 300)
	'<L P="5,50,100,200,300"/>'

	"""
	return Shape("L", thickness, X1, Y1, width, height)

def rectangle(thickness, isFull, X, Y, width, height):
	"""
	Return a rectangle shape.

	Creating a filled rectangle at point (11, 12) of width 30, height 40 and
	thickness 3:

	>>> rectangle(1, Shape.Full, 11, 12, 30, 40)
	'<R P="3,11,12,30,40,1"/>'

	An empty one:

	>>> rectangle(1, Shape.Empty, 11, 12, 30, 40)
	'<R P="3,11,12,30,40,0"/>'

	"""
	return _FullOrEmptyShape(_FullOrEmptyShape.Rectangle, thickness, isFull, \
							 X, Y, width, height)

def ellipse(thickness, isFull, X, Y, width, height):
	"""
	Return an ellipse shape.

	Creating a filled ellipse at point (11, 12) of width 30, height 40 and
	thickness 3:

	>>> ellipse(1, Shape.Full, 11, 12, 30, 40)
	'<R P="3,11,12,30,40,1"/>'

	An empty one:

	>>> ellipse(1, Shape.Empty, 11, 12, 30, 40)
	'<R P="3,11,12,30,40,0"/>'

	"""
	return _FullOrEmptyShape(_FullOrEmptyShape.Ellipse, thickness, isFull, \
							 X, Y, width, height)

def curve(thickness, X1, Y1, pivotX, pivotY, X2, Y2):
	"""
	Return a curve shape.

	Creating a curve between points (0, 0) and (400, 200) of thickness 5 with
	a pivot point at (300, 100)

	>>> curve(5, 0, 0, 300, 100, 400, 200)
	'<C P="5,0,0,300,100,400,200"/>'

	"""
	return _Curve(thickness, X1, Y1, pivotX, pivotY, X2, Y2)

SHAPE_TAGS = {
		'L' : line,
		'R' : rectangle,
		'E' : ellipse,
		'C' : curve
	}

def make_shape(tag, *args):
	"""
	Return the shape corresponding to the letter ``tag`` instanciated
	with arguments ``args``.

	This is mainly used as an helper function.

	"""
	return SHAPE_TAGS[tag](*args)


class Map():
	"""
	A map class containing all free shapes and groups of shapes.

	Shapes and groups can be added, removed, and the map can be laoded
	and saved respectively from and to files or strings.

	"""

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
		"""
		Return the number of shapes in the map.
		Sum up free shapes and grouped shapes.

		"""
		return len(self.shapes) + sum(map(len, self.groups))

	def add(self, *shapes):
		"""
		Add some free shapes or groups to a map.

		>>> m = Map()
		>>> m.add(line(1,0,0,100,100))
		>>> m.add(mycurve, mygroup, myrectangle)

		"""
		for s in shapes:
			if isinstance(s, Group):
				self.groups.append(s)
			else:
				self.shapes.append(s)

	def remove(self, shape):
		"""
		Remove a free shape or a group from a map.

		>>> m = Map()
		>>> l = line(1,0,0,100,100)
		>>> m.add(l)
		>>> len(m)
		1
		>>> m.remove(l)
		>>> len(m)
		0

		"""
		if isinstance(shape, Group):
			self.groups.remove(shape)
		else:
			self.shapes.remove(shape)

	def to_file(self, filename):
		"""
		Save the code of the map to the file filename.

		"""
		with open(filename, "w") as save_file:
			save_file.write(str(self).encode('utf8'))

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
	def _build(root):
		m = Map()

		free_shapes = root.find('F')	# tous les enfants de la balise <F>
		for s in free_shapes:			# à savoir les formes libres
			shape = Map._make_shape(s)
			m.add(shape)

		return m

	@staticmethod
	def from_file(filename):
		"""
		Create a map from a code contained in the file filename.

		>>> m = Map.from_file("mymap.txt")

		"""

		tree = ET.parse(filename)

		return Map._build(tree.getroot())

	@staticmethod
	def from_string(data):
		"""
		Create a map from a string containing the map code.

		>>> data = '<C><G/><F><L P="5,0,0,100,100"/></F></C>'
		>>> m = Map.from_string(data)

		"""

		root = ET.fromstring(data)

		return Map._build(root)
