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
		self.setSelected(not self.selected)



class AliasedShape(Shape):


	def __init__(self):
		Shape.__init__(self)

	def repaint(self, parentClass, painter, option, widget=0):
		hints = painter.renderHints()
		painter.setRenderHint(QPainter.Antialiasing, False)
		parentClass.paint(self, painter, option, widget)
		painter.setRenderHints(hints)



class RectItem(QGraphicsRectItem, Shape):


	def __init__(self, *args):
		QGraphicsRectItem.__init__(self, *args)
		AliasedShape.__init__(self)

	def paint(self, painter, option, widget=0):
		hints = painter.renderHints()
		painter.setRenderHint(QPainter.Antialiasing, False)
		QGraphicsRectItem.paint(self, painter, option, widget)
		painter.setRenderHints(hints)


class LineItem(QGraphicsLineItem, Shape):


	def __init__(self, *args):
		QGraphicsLineItem.__init__(self, *args)
		Shape.__init__(self)


class EllipseItem(QGraphicsEllipseItem, Shape):


	def __init__(self, *args):
		QGraphicsEllipseItem.__init__(self, *args)
		Shape.__init__(self)



class CurveItem(QGraphicsPixmapItem, Shape):


	def __init__(self, x, y):
		self.start = QPointF(x, y)
		QGraphicsPixmapItem.__init__(self)
		Shape.__init__(self)
		self.setShapeMode(QGraphicsPixmapItem.MaskShape)
		self.path = QPainterPath()
		self.path.moveTo(x, y)

	def setPen(self, pen):
		self.pen = pen

	def set_end(self, x, y):
		self.end = QPointF(x, y)

	def set_anchor(self, x, y):
		self.anchor = QPointF(x, y)

	def setup(self):
		self.anchor1 = self.start + (2/3) * (self.anchor - self.start)
		self.anchor2 = self.end + (2/3) * (self.anchor - self.end)
		self.path = QPainterPath(self.start)
		self.path.cubicTo(self.anchor1, self.anchor2, self.end)

		thickness = self.pen.width()
		rect = self.path.boundingRect()
		rect.setWidth(rect.width()+thickness)
		rect.setHeight(rect.height()+thickness)
		canvas = QImage(rect.size().toSize(), QImage.Format_ARGB32)
		canvas.fill(QColor(0,0,0,0))
		painter = QPainter(canvas)
		painter.setPen(self.pen)
		painter.drawPath(self.path.translated(-rect.topLeft()))
		painter.end()
		self.result = QPainterPath()
		self.setPixmap(QPixmap.fromImage(canvas))
		self.setPos(self.start)
