from PyQt5 import QtCore, QtGui, QtWidgets
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
from track_model import TrackModel
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
# from Track_Model_Block_Test import Ui_Track_Model_Block
# from Track_Model_Train_Test import Ui_Track_Model_Train
from api.track_controller_track_model_api import TrackControllerTrackModelAPI
from api.track_model_train_model_api import TrackModelTrainModelAPI

class Ui_TrackModel_MainUI(QMainWindow):
    def __init__(self, track_model: TrackModel):
        super().__init__()
        self.track_model = track_model
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(780, 435)
        # self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.block_title = QtWidgets.QLabel(self.centralwidget)
        self.block_title.setGeometry(QtCore.QRect(320,75,450,30))
        self.block_title.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                                       "border: 2px solid black;\n"
                                       "font-style: bold;\n"
                                       "font-size: 16pt;")
        self.block_title.setAlignment(QtCore.Qt.AlignCenter)

        self.train_title = QtWidgets.QLabel(self.centralwidget)
        self.train_title.setGeometry(QtCore.QRect(320, 235, 450, 30))
        self.train_title.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                                       "border: 2px solid black;\n"
                                       "font-style: bold;\n"
                                       "font-size: 16pt;")
        self.train_title.setAlignment(QtCore.Qt.AlignCenter)
        self.train_title.setText("Search by Train")

        self.block_title.setText("Search by Block")
        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(0, 0, 781, 71))
        self.title.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                 "border: 3px solid black;\n")

        self.title.setObjectName("title")
        tfont = QtGui.QFont()
        tfont.setPointSize(16)
        tfont.setBold(True)
        tfont.setWeight(75)
        self.title.setFont(tfont)
        self.testbench = QtWidgets.QPushButton(self.centralwidget)
        self.testbench.setGeometry(QtCore.QRect(340, 10, 131, 41))
        self.testbench.setObjectName("testbench")
        self.testbench.setStyleSheet("border: 1px solid black;")
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.testbench.setFont(font)
        self.system_speed = QtWidgets.QLabel(self.centralwidget)
        self.system_speed.setGeometry(QtCore.QRect(600, 10, 171, 41))
        self.system_speed.setObjectName("system_speed")
        self.system_speed.setFont(font)
        self.system_speed.setStyleSheet("border: 1px solid black;")
        self.clock = QtWidgets.QLabel(self.centralwidget)
        self.clock.setGeometry(QtCore.QRect(480, 10, 111, 41))
        self.clock.setObjectName("clock")
        self.clock.setFont(font)
        self.clock.setStyleSheet("border: 1px solid black;")
        self.doubleSpinBox = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.doubleSpinBox.setGeometry(QtCore.QRect(700, 20, 62, 22))
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.doubleSpinBox.setStyleSheet("border: 1px solid black;")
        self.track_map = QtWidgets.QLabel(self.centralwidget)
        self.track_map.setGeometry(QtCore.QRect(0, 80, 311, 291))
        self.track_map.setStyleSheet("image: url(:/track_map/track map.PNG);\n"
                                     "image: url(:/map/track map.png);")
        self.track_map.setText("")
        self.track_map.setPixmap(QtGui.QPixmap(":/track_map/track map.PNG"))
        self.track_map.setScaledContents(True)
        self.track_map.setObjectName("track_map")
        pixmap = QPixmap('track map.png')
        self.track_map.setPixmap(pixmap)
        self.track_map.setStyleSheet("border: 1px solid black;")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(320, 220, 461, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line_color = QtWidgets.QComboBox(self.centralwidget)
        self.line_color.setGeometry(QtCore.QRect(330, 110, 91, 61))
        self.line_color.setObjectName("line_color")
        line_color_list = ["Red", "Green", "Blue"]
        self.line_color.addItems(line_color_list)
        self.line_color.setEditable(False)
        self.line_color.setPlaceholderText("Line Color")  # TODO Find a way to add placeholder text
        self.line_color.setStyleSheet("border: 1px solid black;")

        self.section = QtWidgets.QComboBox(self.centralwidget)
        self.section.setGeometry(QtCore.QRect(440, 110, 91, 61))
        self.section.setObjectName("section")
        self.section.setStyleSheet("border: 1px solid black;")
        section_list_blue = ['A', 'B', 'C', ]
        section_list_red = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T']
        section_list_green = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

        self.block_number = QtWidgets.QComboBox(self.centralwidget)
        self.block_number.setGeometry(QtCore.QRect(550, 110, 91, 61))
        self.block_number.setObjectName("block_number")
        block_list = ['1', '2', '3', '4', '5']
        self.block_number.addItems(block_list)
        self.block_number.setStyleSheet("border: 1px solid black;")

        self.train_selection = QtWidgets.QComboBox(self.centralwidget)
        self.train_selection.setGeometry(QtCore.QRect(330, 280, 201, 61))
        self.train_selection.setObjectName("train_selection")
        train_list = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.train_selection.addItems(train_list)
        self.train_selection.setStyleSheet("border: 1px solid black;")

        self.block_button = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_block_window())
        self.block_button.setGeometry(QtCore.QRect(670, 110, 101, 71))
        self.block_button.setObjectName("block_button")
        self.block_button.setStyleSheet("border: 1px solid black;")


        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.open_train_window())
        self.pushButton_2.setGeometry(QtCore.QRect(670, 280, 101, 71))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet("border: 1px solid black;")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 780, 18))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("TrackModel_MainUI", "Track Model"))
        self.title.setText(_translate("TrackModel_MainUI", "Track Map"))
        self.testbench.setText(_translate("TrackModel_MainUI", "Testbench"))
        self.system_speed.setText(_translate("TrackModel_MainUI", "System Speed"))
        self.clock.setText(_translate("TrackModel_MainUI", "13:56:54"))

    # Update block selection on block_button
    def update_block_button(self):
        c1 = self.line_color.currentText()
        c2 = self.section.currentText()
        c3 = self.block_number.currentText()
        combined_text = f"{c1}{c2}{c3}"
        self.block_button.setText(combined_text)
        self.block_button.setStyleSheet("background: rgb(0,255,0);\n"
                                        "color: white;\n"
                                        "font-style: bold;\n"
                                        "font-size: 16pt;")

    def update_train_button(self):
        c1 = self.train_selection.currentText()
        self.pushButton_2.setText(c1)
        self.pushButton_2.setStyleSheet("background: rgb(0,255,0);\n"
                                        "color: white;\n"
                                        "font-style: bold;\n"
                                        "font-size: 16pt;")

    #Connecting block button to block window
    def open_block_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Track_Model_Block()
        self.ui.setUi(self.window)
        self.window.show()

    #Connecting train button to train window
    def open_train_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Track_Model_Train()
        self.ui.setpUi(self.window)
        self.window.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    e = Ui_TrackModel_MainUI(TrackModel(TrackControllerTrackModelAPI(), TrackModelTrainModelAPI()))
    # TrackModel_MainUI = QtWidgets.QMainWindow()
    # ui = Ui_TrackModel_MainUI()
    # ui.setupUi(TrackModel_MainUI)
    e.line_color.activated.connect(e.update_block_button)
    e.section.activated.connect(e.update_block_button)
    e.block_number.activated.connect(e.update_block_button)
    e.train_selection.activated.connect(e.update_train_button)

    # TrackModel_MainUI.show()
    sys.exit(app.exec_())
    # ui.comboBox1.activated.connect(ui.updatePushButtonText)
