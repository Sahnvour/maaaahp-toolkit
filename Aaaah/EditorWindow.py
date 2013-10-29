import sys
from .base.primitives import *
from .items import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .MainWindow import Ui_MainWindow

class MouseMode():
	Free = 0
	Line = 1
	Curve = 2
	Curve2 = 3
	Rectangle = 4
	Ellipse = 5


class EditorWindow(QMainWindow):

	mouse_modes = {
		'line' : MouseMode.Line,
		'curve' : MouseMode.Curve,
		'rectangle' : MouseMode.Rectangle,
		'ellipse' : MouseMode.Ellipse }


	def __init__(self, parent=None):
		super(EditorWindow, self).__init__(parent)
		self.setup()

	def setup(self):
		# Load UI
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.setup_scene()
		self.setup_signals()

	def setup_scene(self):
		self.map_scene = QGraphicsScene()
		self.map_scene.setBackgroundBrush(QColor(48, 48, 54))
		self.ui.map_view.setScene(self.map_scene)
		self.ui.map_view.setSceneRect(QRectF(0, 0, 800, 400))
		self.ruler = [AliasedLineItem(0, 0, 800, 0), AliasedLineItem(0, 0, 0, 400)]
		pen = QPen(QColor(255, 0, 0))
		for line in self.ruler:
			line.setPen(pen)
		self.mouse_mode = MouseMode.Free

		self.preview_shape = None

	def setup_signals(self):
		# Set signals for primitive shapes
		for button in self.ui.primitives_group.buttons():
			button.clicked.connect(self.shape_changed)

		self.ui.clipboard.clicked.connect(self.to_clipboard)
		self.ui.thickness.valueChanged.connect(self.thickness_changed)
		self.ui.ruler.stateChanged.connect(self.show_ruler)
		self.ui.isFull.stateChanged.connect(self.full_shapes)
		self.ui.opacity.valueChanged.connect(self.opacity_changed)

		# Shortcuts
		self.shortcuts = {}
		shortcut = QShortcut(QKeySequence("Ctrl+M"), self)
		shortcut.activated.connect(self.quality_inf)
		self.shortcuts["Ctrl+M"] = shortcut
		shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
		shortcut.activated.connect(self.quality_sup)
		self.shortcuts["Ctrl+H"] = shortcut

	def eventFilter(self, source, event):
		if event.type() == QEvent.MouseMove:
			pos = self.ui.map_view.mapFromGlobal(event.globalPos())
			self.ui.statusbar.showMessage("({0};{1})".format(pos.x(), pos.y()))
			if self.ui.ruler.isChecked:
				self.ruler[0].setY(pos.y())
				self.ruler[1].setX(pos.x())
				self.ui.map_view.repaint()

			if self.mouse_mode in [MouseMode.Line, MouseMode.Curve]:
				l = self.preview_shape
				l.setLine(l.line().x1(), l.line().y1(), pos.x(), pos.y())

			elif self.mouse_mode in [MouseMode.Rectangle, MouseMode.Ellipse]:
				r = self.preview_shape
				origin = self.editor.points[0] # dirty hack
				x, y = origin[0], origin[1]
				width, height = pos.x() - x, pos.y() - y
				r.setRect(QRectF(x, y, width, height).normalized())

			elif self.mouse_mode == MouseMode.Curve2:
				c = self.preview_shape
				c.set_anchor(pos.x(), pos.y())
				c.setup()

		elif event.type() == QEvent.MouseButtonPress: # Mouse button press
			if source is self.ui.map_view: # from map
				if self.mouse_mode == MouseMode.Free: # and not drawing anything
					self.mouse_mode = self.get_mouse_mode() # switch to what we're drawing
					pos = self.ui.map_view.mapFromGlobal(event.globalPos())
					self.editor.add_point(pos)
					
					# When drawing a curve, preview a line instead
					if self.mouse_mode == MouseMode.Curve:
						# dirty hacks, you should be used to it by now
						points = self.editor.points[:]
						points.append([pos.x(), pos.y()])
						points = [num for elem in points for num in elem]
						self.preview_shape = QGraphicsLineItem(*points[:4])
						pen = QPen(QColor(), self.editor.thickness, Qt.SolidLine, Qt.SquareCap)
						self.preview_shape.setPen(pen)
					# or draw the correct shape
					else:
						self.preview_shape = self.editor.make_item([pos.x(), pos.y()]*3)
					self.add_shape(self.preview_shape)

				elif self.mouse_mode == MouseMode.Curve2:
					self.mouse_mode = MouseMode.Free
					pos = self.ui.map_view.mapFromGlobal(event.globalPos())
					self.remove_shape(self.preview_shape)
					self.editor.add_point(pos)
					self.ui.map_view.repaint()
					
		elif event.type() == QEvent.MouseButtonRelease:
			if self.mouse_mode in [MouseMode.Line, MouseMode.Rectangle, MouseMode.Ellipse]:
				self.mouse_mode = MouseMode.Free
				self.remove_shape(self.preview_shape)
				pos = self.ui.map_view.mapFromGlobal(event.globalPos())
				self.editor.add_point(pos)
				self.ui.map_view.repaint()
			elif self.mouse_mode == MouseMode.Curve:
				self.mouse_mode = MouseMode.Curve2
				pos = self.ui.map_view.mapFromGlobal(event.globalPos())
				self.editor.add_point(pos)
				self.remove_shape(self.preview_shape)
				points = [num for elem in self.editor.points for num in elem]
				points = points + [pos.x(), pos.y()]
				self.preview_shape = self.editor.make_item(points)
				self.preview_shape.setup()
				self.add_shape(self.preview_shape)
				
		elif event.type() == QEvent.KeyRelease:
			if event.key() == Qt.Key_Space:
				t = QTransform()
				t.scale(2,2)
				self.ui.map_view.setTransform(t)

		return QMainWindow.eventFilter(self, source, event)

	def add_shape(self, shape):
		self.map_scene.addItem(shape)

	def remove_shape(self, shape):
		self.map_scene.removeItem(shape)

	def get_mouse_mode(self):
		name = self.ui.primitives_group.checkedButton().objectName()
		if name in self.mouse_modes.keys():
			return self.mouse_modes[name]
		else:
			return MouseMode.Free

	@pyqtSlot()
	def to_clipboard(self):
		to_clipboard(self.editor.map)

	@pyqtSlot()
	def shape_changed(self):
		self.editor.set_shape(self.sender().objectName())

	@pyqtSlot(int)
	def thickness_changed(self, value):
		self.editor.set_thickness(value)

	@pyqtSlot(int)
	def show_ruler(self, state):
		for l in self.ruler:
			if state:
				self.add_shape(l)
			else:
				self.remove_shape(l)

	@pyqtSlot(int)
	def full_shapes(self, state):
		self.editor.set_full(state)

	@pyqtSlot(int)
	def opacity_changed(self, value):
		self.setWindowOpacity((100 - value) / 100)

	@pyqtSlot()
	def quality_inf(self):
		self.ui.map_view.setRenderHints(QPainter.NonCosmeticDefaultPen)

	@pyqtSlot()
	def quality_sup(self):
		self.ui.map_view.setRenderHints(QPainter.Antialiasing)
