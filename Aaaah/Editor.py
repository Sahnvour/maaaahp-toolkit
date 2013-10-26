import sys
import inspect
from EditorWindow import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import base.primitives as prim
import base.composites as comp
import base.generators as gen

shapes = {
	'line' 		: {'func' : prim.line, 'points' : 2},

	'curve' 	: {'func' : prim.curve, 'points' : 3},

	'rectangle' : {'func' : prim.rectangle, 'points' : 2},

	'ellipsis' 	: {'func' : prim.ellipsis, 'points' : 2}
	}

class Editor():


	def __init__(self):
		self.app = QApplication(sys.argv)
		self.mainWindow = EditorWindow()
		self.mainWindow.show()
		self.app.installEventFilter(self.mainWindow)
		self.mainWindow.editor = self

		self.map = prim.Map()

		self.points = []
		self.thickness = 1
		self.isFull = Shape.Empty
		self.shape = shapes['line']
	
	def run(self):
		sys.exit(self.app.exec_())

	def set_shape(self, name):
		self.points.clear()
		if name in shapes.keys():
			self.shape = shapes[name]
		else:
			raise RuntimeError("{} is not a valid shape name".format(name))

	def set_point(self, pos):
		if self.shape is None:
			return

		self.points.append([pos.x(), pos.y()])

		if len(self.points) == self.shape['points']:
			self.process_shape()
			self.points.clear()

	def set_thickness(self, value):
		self.thickness = value

	def set_full(self, value):
		self.isFull = Shape.Full if value else Shape.Empty

	def process_shape(self):
		points = [num for elem in self.points for num in elem]
		shape = self.make_shape(points)
		self.map.add(shape)
		print(shape)
		#item = self.shape_to_item(name, shape, points)
		#self.mainWindow.add_item()

	def make_shape(self, points):
		if self.shape['func'] is line:
			points[2] = points[2] - points[0]
			points[3] = points[3] - points[1]
			return prim.line(self.thickness, *points)

		elif self.shape['func'] is prim.curve:
			points[2] = points[2] - points[0]
			points[3] = points[3] - points[1]
			points[4] = points[4] - points[0]
			points[5] = points[5] - points[1]
			return prim.curve(self.thickness, *points)

		elif self.shape['func'] is prim.rectangle:
			points[2] = points[2] - points[0]
			points[3] = points[3] - points[1]
			return prim.rectangle(self.thickness, self.isFull, *points)

		elif self.shape['func'] is prim.ellipsis:
			points[2] = points[2] - points[0]
			points[3] = points[3] - points[1]
			return prim.ellipsis(self.thickness, self.isFull, *points)

		raise RuntimeError("the shape wasnt a primitive one, this should never happen")


if __name__ == "__main__":
	Editor().run()