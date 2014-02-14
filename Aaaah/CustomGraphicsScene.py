from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CustomGraphicsScene(QGraphicsScene):


	mouseClicked = pyqtSignal(QPointF)
	mouseReleased = pyqtSignal(QPointF)
	mouseMoved = pyqtSignal(QPointF)


	def __init__(self):
		super(QGraphicsScene, self).__init__()
		
		self.selection = []
		self.offsets = []
		self.multi_select = False
		self.select_point = None
		self.dragging = False

	def mousePressEvent(self, event):
		if event.button() == Qt.LeftButton and event.buttons() == Qt.LeftButton:
			self.mouseClicked.emit(event.scenePos())
		else:
			item = self.itemAt(event.scenePos(), QTransform())
			if item:
				self.selection.append(item)
		QGraphicsScene.mousePressEvent(self, event)

	def mouseReleaseEvent(self, event):
		if event.button() == Qt.LeftButton:
			self.mouseReleased.emit(event.scenePos())
		QGraphicsScene.mouseReleaseEvent(self, event)

	def mouseMoveEvent(self, event):
		self.mouseMoved.emit(event.scenePos())

		QGraphicsScene.mouseMoveEvent(self, event)
