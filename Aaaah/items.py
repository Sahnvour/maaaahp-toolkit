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



class Shape():


	def __init__(self):
		self.setBoundingRegionGranularity(1)
		self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)
		self.setAcceptedMouseButtons(Qt.RightButton)
		self.last_click = None
		self.selected = False

	def set_shape(self, shape):
		self.shape = shape

	def set_pos(self, point):
		old_pos = self.pos()
		self.setPos(point)

	def mousePressEvent(self, event):
		pass

	def mouseReleaseEvent(self, event):
		self.selected = not self.selected
		self.setSelected(self.selected)

	def setup(self):
		pass


class RectItem(QGraphicsRectItem, Shape):


	def __init__(self, *args):
		QGraphicsRectItem.__init__(self, *args)
		Shape.__init__(self)

	def setup(self):
		self.setup_picking()

	def setup_picking(self):
		r = self.rect()
		thick = self.shape.thickness
		topLeft = QPointF(r.topLeft()) + QPointF(thick/2+1, thick/2+1)
		size = QSizeF(r.size()) - QSizeF(thick, thick)
		self.holeRect = QRectF(topLeft, size)
		print(str(self.rect()))
		print(str(self.holeRect))
		item = QGraphicsRectItem(self.holeRect)
		item.setBrush(QColor(255, 0, 0))
		item.setParentItem(self)

	def paint(self, painter, option, widget=0):
		hints = painter.renderHints()
		painter.setRenderHint(QPainter.Antialiasing, False)
		QGraphicsRectItem.paint(self, painter, option, widget)
		painter.setRenderHints(hints)

	def contains(self, pos):
		if self.shape.isFull:
			return self.rect().contains(pos)
		else:
			outline = self.rect().contains(pos)
			hole = self.holeRect.contains(pos)
			print("outline:", outline, "hole:", hole)
			return False
			return outline and not hole


class LineItem(QGraphicsLineItem, Shape):


	def __init__(self, *args):
		QGraphicsLineItem.__init__(self, *args)
		Shape.__init__(self)



class EllipseItem(QGraphicsEllipseItem, Shape):


	def __init__(self, *args):
		QGraphicsEllipseItem.__init__(self, *args)
		Shape.__init__(self)



class CurveItem(QGraphicsPathItem, Shape):


	def __init__(self, x, y):
		self.start = QPointF(x, y)
		QGraphicsPathItem.__init__(self)
		Shape.__init__(self)

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