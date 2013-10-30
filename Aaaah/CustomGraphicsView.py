from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CustomGraphicsView(QGraphicsView):


	def __init__(self, editor_window, *args):
		super().__init__(*args)

		self.editor_window = editor_window

		self.selection = []
		self.offsets = []
		self.multi_select = False
		self.select_point = None
		self.dragging = False

		self.setGeometry(QRect(10, 10, 802, 402))
		self.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
		self.setMouseTracking(True)
		self.setAutoFillBackground(False)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setRenderHints(QPainter.Antialiasing)
		self.setObjectName("map_view")

	def mousePressEvent(self, event):
		pos = self.mapFromGlobal(event.globalPos())
		modifiers = event.modifiers()

		if event.button() == Qt.LeftButton:
			self.editor_window.draw_click(event)

		elif event.button() == Qt.RightButton:
			self.select_point = pos
			for s in self.selection:
				if s.contains(pos): # deselect or drag
					for s in self.selection: # construct the offsets for dragging
						self.offsets = [s.pos() - pos for s in self.selection]
					break

	def mouseReleaseEvent(self, event):
		pos = self.mapFromGlobal(event.globalPos())
		modifiers = event.modifiers()

		if event.button() == Qt.LeftButton:
			self.editor_window.draw_release(event)

		elif event.button() == Qt.RightButton:
			if self.select_point == pos: # one click selection
					self.update_selection(pos)
			if self.offsets:
				self.offsets.clear()

	def mouseMoveEvent(self, event):
		pos = self.mapFromGlobal(event.globalPos())
		modifiers = event.modifiers()

		if event.buttons() == Qt.RightButton:
			if not self.offsets:
				for s in self.selection:
					self.offsets = [s.pos() - pos for s in self.selection]

			for s, off in zip(self.selection, self.offsets):
				s.set_pos(pos + off)

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
