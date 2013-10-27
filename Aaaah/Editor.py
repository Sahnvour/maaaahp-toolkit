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

	'ellipse' 	: {'func' : prim.ellipse, 'points' : 2}
	}

class Editor():


	def __init__(self):
		self.app = QApplication(sys.argv)
		self.mainWindow = EditorWindow()
		self.mainWindow.show()
		self.app.installEventFilter(self.mainWindow)
		self.mainWindow.editor = self

		self.map = prim.Map()
		self.shapes = [] # listing tuples as (shape, item)

		self.points = []
		self.pens = {}
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
		
		item = self.make_item(points[:])
		shape = self.make_shape(points[:])
		self.map.add(shape)
		self.mainWindow.add_item(item)

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

		elif self.shape['func'] is prim.ellipse:
			points[2] = points[2] - points[0]
			points[3] = points[3] - points[1]
			return prim.ellipse(self.thickness, self.isFull, *points)

		raise RuntimeError("the shape wasnt a primitive one, this should never happen")

	def make_item(self, points):
		pen = None
		item = None

		if self.shape['func'] is line:
			item = QGraphicsLineItem(*points[:4])
			pen = QPen(QColor(), self.thickness, Qt.SolidLine, Qt.RoundCap)

		elif self.shape['func'] is prim.curve:
			raise NotImplemented()

		elif self.shape['func'] is prim.rectangle:
			points[2] = points[2] - points[0]
			points[3] = points[3] - points[1]
			item = AliasedRectItem(*points[:4])
			pen = QPen(QColor(), self.thickness, Qt.SolidLine, Qt.SquareCap)
			pen.setJoinStyle(Qt.MiterJoin)

		elif self.shape['func'] is prim.ellipse:
			points[2] = points[2] - points[0]
			points[3] = points[3] - points[1]
			item = QGraphicsEllipseItem(*points[:4])
			pen = QPen(QColor(), self.thickness, Qt.SolidLine, Qt.SquareCap)

		else:
			raise RuntimeError("the shape wasnt a primitive one, this should never happen")

		item.setPen(pen)
		if self.isFull:
			item.setBrush(QColor(0,0,0))

		return item

if __name__ == "__main__":
	Editor().run()