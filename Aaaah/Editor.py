import sys
from .EditorWindow import *
from .items import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .base import primitives as prim
from .base import composites as comp
from .base import generators as gen

def make_line(thickness, points):
	item = LineItem(*points[:4])
	pen = QPen(QColor(), thickness, Qt.SolidLine, Qt.RoundCap)
	item.setPen(pen)

	return item, pen

def make_curve(thickness, points):
	points = [points[i] for i in [0, 1, 4, 5, 2, 3]]
	item = CurveItem(*points[:2])
	item.set_anchor(*points[2:4])
	item.set_end(*points[4:])
	pen = QPen(QColor(), thickness, Qt.SolidLine, Qt.RoundCap)
	item.setPen(pen)
	item.setup()

	return item, pen

def make_rectangle(thickness, points):
	points[2] = points[2] - points[0]
	points[3] = points[3] - points[1]
	item = RectItem(*points[:4])
	pen = QPen(QColor(), thickness, Qt.SolidLine, Qt.SquareCap)
	pen.setJoinStyle(Qt.MiterJoin)
	item.setPen(pen)

	return item, pen

def make_ellipse(thickness, points):
	points[2] = points[2] - points[0]
	points[3] = points[3] - points[1]
	item = EllipseItem(*points[:4])
	pen = QPen(QColor(), thickness, Qt.SolidLine, Qt.SquareCap)
	item.setPen(pen)

	return item, pen

shapes = {
	'line' 		: {'func' : prim.line, 'points' : 2, 'make' : make_line},

	'curve' 	: {'func' : prim.curve, 'points' : 3, 'make' : make_curve},

	'rectangle' : {'func' : prim.rectangle, 'points' : 2, 'make' : make_rectangle},

	'ellipse' 	: {'func' : prim.ellipse, 'points' : 2, 'make' : make_ellipse}
	}

class Editor():


	def __init__(self):
		self.app = QApplication(sys.argv)
		self.mainWindow = EditorWindow()
		self.mainWindow.show()
		self.mainWindow.editor = self

		self.map = prim.Map()
		self.shapes = [] # listing tuples as (shape, item)

		self.points = []
		self.pens = {}
		self.thickness = 1
		self.isFull = prim.Shape.Empty
		self.shape = shapes['line']
	
	def run(self):
		sys.exit(self.app.exec_())

	def set_shape(self, name):
		self.points.clear()
		self.shape = shapes[name]

	def add_point(self, pos):
		if self.shape is None:
			return
		
		self.points.append([pos.x(), pos.y()])

		if len(self.points) == self.shape['points']:
			self.process_shape()
			self.points.clear()

	def set_thickness(self, value):
		self.thickness = value

	def set_full(self, value):
		self.isFull = prim.Shape.Full if value else prim.Shape.Empty

	def process_shape(self):
		points = [num for elem in self.points for num in elem]
		
		item = self.make_item(points[:])
		shape = self.make_shape(points[:])
		item.set_shape(shape)
		self.map.add(shape)
		self.mainWindow.map_scene.addItem(item)

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
			pts = [points[i] for i in [0, 1, 4, 5, 2, 3]]
			return prim.curve(self.thickness, *pts)

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
		item, pen = self.shape['make'](self.thickness, points)

		if self.isFull and self.shape['func'] in [prim.rectangle, prim.ellipse]:
			item.setBrush(QColor(0,0,0))

		return item




if __name__ == "__main__":
	Editor().run()