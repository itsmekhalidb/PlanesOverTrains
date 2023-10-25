import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore
from api.launcher import Launcher

QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QApplication(sys.argv)
e = Launcher()
sys.exit(app.exec_())

# comment for lucas's dumbass to be able to pull again