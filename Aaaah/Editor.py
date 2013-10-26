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

		self.points = []
		self.thickness = 1
		self.isFull = Shape.Empty
		self.shape = shapes['line']
	
	def run(self):
		sys.exit(self.app.exec_())

	def set_shape(self, name):
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

	def process_shape(self):
		points = [num for elem in self.points for num in elem]
		func = self.shape['func']
		args = inspect.getargspec(func)[0]
		if 'isFull' in args:
			shape = func(self.thickness, self.isFull, *points)
		else:
			shape = func(self.thickness, *points)
		print(shape)
		#item = self.shape_to_item(name, shape, points)
		#self.mainWindow.add_item()

	def shape_to_item(self, shape, points):
		item = None
		if self.shape['func'] is line:
			item = QGraphicsLineItem()
		elif self.shape['func'] is prim.curve:
			1
		elif self.shape['func'] is prim.rectangle:
			1
		elif self.shape['func'] is prim.ellipsis:
			1
		return item


if __name__ == "__main__":
	Editor().run()