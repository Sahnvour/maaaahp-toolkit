from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class AliasedRectItem(QGraphicsRectItem):


	def __init__(self, *args):
		super().__init__(*args)

	def paint(self, painter, option, widget=0):
		hints = painter.renderHints()
		painter.setRenderHint(QPainter.Antialiasing, False)
		super().paint(painter, option, widget)
		painter.setRenderHints(hints)


class AliasedLineItem(QGraphicsLineItem):


	def __init__(self, *args):
		super().__init__(*args)

	def paint(self, painter, option, widget=0):
		hints = painter.renderHints()
		painter.setRenderHint(QPainter.Antialiasing, False)
		super().paint(painter, option, widget)
		painter.setRenderHints(hints)


class CustomItem():


	def __init__(self):
		self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
		self.setAcceptedMouseButtons(Qt.RightButton)

	def set_shape(self, shape):
		self.selected = False
		self.shape = shape

	def select(self):
		if self.selected:
			self.selected = False
			self.pen().setColor(QColor(0, 0, 0))
			try:
				self.setBrush(QColor(0, 0, 0))
			except AttributeError:
				pass
		else:
			self.selected = True
			self.pen().setColor(QColor(255, 255, 255))
			try:
				self.setBrush(QColor(255, 255, 255))
			except AttributeError:
				pass

	def set_pos(self, point):
		old_pos = self.pos()
		self.setPos(point)

	def setSelected(self, value):
		print("selected")
		super().setSelected(value)



class CustomRectItem(AliasedRectItem, CustomItem):


	def __init__(self, *args):
		super(AliasedRectItem, self).__init__(*args)
		super(CustomItem, self).__init__()


class CustomLineItem(QGraphicsLineItem, CustomItem):


	def __init__(self, *args):
		super(QGraphicsLineItem, self).__init__(*args)
		super(CustomItem, self).__init__()


class CustomEllipseItem(QGraphicsEllipseItem, CustomItem):


	def __init__(self, *args):
		super(QGraphicsEllipseItem, self).__init__(*args)
		super(CustomItem, self).__init__()


class CustomCurveItem(QGraphicsPathItem, CustomItem):


	def __init__(self, x, y):
		self.start = QPointF(x, y)
		super(QGraphicsPathItem, self).__init__()
		super(CustomItem, self).__init__()

	def set_start(self, x, y):
		self.start = QPointF(x, y)
		self.path().moveTo(self.start)

	def set_end(self, x, y):
		self.end = QPointF(x, y)

	def set_anchor(self, x, y):
		self.anchor = QPointF(x, y)

	def setup(self):
		self.anchor1 = self.start + (2/3) * (self.anchor - self.start)
		self.anchor2 = self.end + (2/3) * (self.anchor - self.end)
		path = QPainterPath(self.start)
		path.cubicTo(self.anchor1, self.anchor2, self.end)
		self.setPath(path)