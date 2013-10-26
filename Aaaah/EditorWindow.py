import sys
from base.primitives import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MainWindow import Ui_MainWindow


class EditorWindow(QMainWindow):


	def __init__(self, parent=None):
		super(EditorWindow, self).__init__(parent)
		self.setup()

	def setup(self):
		# Load UI
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.clipboard.clicked.connect(self.to_clipboard)

		self.setup_scene()
		self.setup_signals()

	def setup_scene(self):
		self.map_scene = QGraphicsScene()
		self.map_scene.setBackgroundBrush(QColor(48, 48, 54))
		self.ui.map_view.setScene(self.map_scene)
		self.ui.map_view.setSceneRect(QRectF(0, 0, 800, 400))
		self.ruler = [QGraphicsLineItem(0, 0, 800, 0), QGraphicsLineItem(0, 0, 0, 400)]
		pen = QPen(QColor(255, 0, 0))
		for line in self.ruler:
			line.setPen(pen)
		self.drawing = False

	def setup_signals(self):
		# Set signals for primitive shapes
		for button in self.ui.primitives_group.buttons():
			button.clicked.connect(self.shape_changed)

		self.ui.thickness.valueChanged.connect(self.thickness_changed)
		self.ui.ruler.stateChanged.connect(self.show_ruler)
		self.ui.isFull.stateChanged.connect(self.full_shapes)

	def eventFilter(self, source, event):
		if event.type() == QEvent.MouseMove:
			pos = self.ui.map_view.mapFromGlobal(event.globalPos())
			self.ui.statusbar.showMessage("({0};{1})".format(pos.x(), pos.y()))
			self.ruler[0].setY(pos.y())
			self.ruler[1].setX(pos.x())

		elif event.type() == QEvent.MouseButtonPress:
			if source is self.ui.map_view:
				self.drawing = True
				pos = event.pos()
				self.editor.set_point(pos)

		elif event.type() == QEvent.MouseButtonRelease and self.drawing:
			self.drawing = False
			pos = event.pos()
			self.editor.set_point(pos)

		return QMainWindow.eventFilter(self, source, event)

	def add_item(self, item):
		self.map_scene.addItem(item)

	@pyqtSlot()
	def to_clipboard(self):
		to_clipboard(self.map)

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


if __name__ == "__main__":

	app = QApplication(sys.argv)
	editor = EditorWindow()
	editor.show()
	app.installEventFilter(editor)
	sys.exit(app.exec_())