import sys
from .base.primitives import *
from .items import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .MainWindow import Ui_MainWindow
from .CustomGraphicsView import CustomGraphicsView

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
		self.ui.map_view = CustomGraphicsView(self, self.map_scene, self.ui.centralwidget)
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
		self.add_shortcut("Ctrl+M", self.quality_inf)
		self.add_shortcut("Ctrl+H", self.quality_sup)

	def add_shortcut(self, command, slot):
		shortcut = QShortcut(QKeySequence(command), self)
		shortcut.activated.connect(slot)
		self.shortcuts[command] = shortcut

	def eventFilter(self, source, event):
		if isinstance(event, QMouseEvent):
			pos = self.ui.map_view.mapFromGlobal(event.globalPos())

		if event.type() == QEvent.MouseMove:
			if event.modifiers() == Qt.ControlModifier:
				self.multi_select = True
			else:
				self.mouse_move(event)
				
		elif event.type() == QEvent.KeyRelease:
			if event.key() == Qt.Key_Space:
				pass

		return QMainWindow.eventFilter(self, source, event)

	def mouse_move(self, event):
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

	def draw_click(self, event):
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
				pen = QPen(QColor(), self.editor.thickness, Qt.SolidLine, Qt.RoundCap)
				self.preview_shape.setPen(pen)
			# or draw the correct shape
			else:
				self.preview_shape = self.editor.make_item([pos.x(), pos.y()]*3)
			self.map_scene.addItem(self.preview_shape)

		elif self.mouse_mode == MouseMode.Curve2:
			self.mouse_mode = MouseMode.Free
			pos = self.ui.map_view.mapFromGlobal(event.globalPos())
			self.map_scene.removeItem(self.preview_shape)
			self.editor.add_point(pos)
			self.ui.map_view.repaint()

	def draw_release(self, event):
		if self.mouse_mode in [MouseMode.Line, MouseMode.Rectangle, MouseMode.Ellipse]:
			self.mouse_mode = MouseMode.Free
			self.map_scene.removeItem(self.preview_shape)
			pos = self.ui.map_view.mapFromGlobal(event.globalPos())
			self.editor.add_point(pos)
			self.ui.map_view.repaint()
		elif self.mouse_mode == MouseMode.Curve:
			self.mouse_mode = MouseMode.Curve2
			pos = self.ui.map_view.mapFromGlobal(event.globalPos())
			self.editor.add_point(pos)
			self.map_scene.removeItem(self.preview_shape)
			points = [num for elem in self.editor.points for num in elem]
			points = points + [pos.x(), pos.y()]
			self.preview_shape = self.editor.make_item(points)
			self.preview_shape.setup()
			self.map_scene.addItem(self.preview_shape)

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
				self.map_scene.addItem(l)
			else:
				self.map_scene.removeItem(l)

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
