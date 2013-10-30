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
		pos = event.scenePos()
		modifiers = event.modifiers()

		if event.button() == Qt.LeftButton:
			self.mouseClicked.emit(pos)

		elif event.button() == Qt.MiddleButton:
			self.select_point = pos
			for s in self.selection:
				if s.contains(pos): # deselect or drag
					for s in self.selection: # construct the offsets for dragging
						self.offsets = [s.pos() - pos for s in self.selection]
					break

	def mouseReleaseEvent(self, event):
		pos = event.scenePos()
		modifiers = event.modifiers()

		if event.button() == Qt.LeftButton:
			self.mouseReleased.emit(pos)

		elif event.button() == Qt.MiddleButton:
			if self.select_point == pos: # one click selection
					self.update_selection(pos)
			if self.offsets:
				self.offsets.clear()

	def mouseMoveEvent(self, event):
		pos = event.scenePos()
		modifiers = event.modifiers()

		if event.buttons() == Qt.MiddleButton:
			if not self.offsets:
				for s in self.selection:
					self.offsets = [s.pos() - pos for s in self.selection]

			for s, off in zip(self.selection, self.offsets):
				s.set_pos(pos + off)
		else:
			self.mouseMoved.emit(pos)

	def update_selection(self, pos):
		for item in self.items():
			if not item.contains(pos):
				continue
			if item.selected:
				self.selection.remove(item)
			else:
				self.selection.append(item)
			item.select()
			break


	def selection(self):
		return self.selection
