import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MainWindow import Ui_MainWindow

class EditorWindow(QMainWindow):
	def __init__(self, parent=None):
		super(EditorWindow, self).__init__(parent)
		self.setup()

	def setup(self):
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

app = QApplication(sys.argv)
editor = EditorWindow()
editor.show()
sys.exit(app.exec_())