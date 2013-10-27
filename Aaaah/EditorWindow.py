import sys
from base.primitives import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MainWindow import Ui_MainWindow

class MouseMode():
	Free = 0
	Line = 1
	Curve = 2
	Rectangle = 3
	Ellipse = 4

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

			if self.mouse_mode == MouseMode.Line:
				l = self.preview_shape
				l.setLine(l.line().x1(), l.line().y1(), pos.x(), pos.y())

			elif self.mouse_mode == MouseMode.Rectangle:
				r = self.preview_shape
				origin = self.editor.points[0] # dirty hack
				x, y = origin[0], origin[1]
				width, height = pos.x() - x, pos.y() - y
				r.setRect(QRectF(x, y, width, height).normalized())

			elif self.mouse_mode == MouseMode.Ellipse:
				e = self.preview_shape
				origin = self.editor.points[0] # dirty hack again
				x, y = origin[0], origin[1]
				width, height = pos.x() - x, pos.y() - y
				e.setRect(QRectF(x, y, width, height).normalized())

		elif event.type() == QEvent.MouseButtonPress and self.mouse_mode == MouseMode.Free:
			if source is self.ui.map_view:
				self.mouse_mode = self.get_mouse_mode()
				pos = self.ui.map_view.mapFromGlobal(event.globalPos())
				self.editor.set_point(pos)
				self.preview_shape = self.editor.make_item([pos.x(), pos.y()]*2)
				self.map_scene.addItem(self.preview_shape)

		elif event.type() == QEvent.MouseButtonRelease:
			if self.mouse_mode in [MouseMode.Line, MouseMode.Rectangle, MouseMode.Ellipse]:
				self.mouse_mode = MouseMode.Free
				self.map_scene.removeItem(self.preview_shape)
				pos = self.ui.map_view.mapFromGlobal(event.globalPos())
				self.editor.set_point(pos)

		return QMainWindow.eventFilter(self, source, event)

	def add_item(self, item):
		self.map_scene.addItem(item)

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


if __name__ == "__main__":

	app = QApplication(sys.argv)
	editor = EditorWindow()
	editor.show()
	app.installEventFilter(editor)
	sys.exit(app.exec_())