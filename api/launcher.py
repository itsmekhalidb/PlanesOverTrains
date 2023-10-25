# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
import sys

# APIs
from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.track_controller_track_model_api import TrackControllerTrackModelAPI
from api.track_model_train_model_api import TrackModelTrainModelAPI
from api.train_model_train_controller_api import TrainModelTrainControllerAPI


# from CTC.ctc import CTC
from track_controller.track_controller import Track_Controller
# from track_controller_hw.track_controller_hw import TrackControllerHW
# from track_model.track_model import TrackModel

# Managers are only necessary for train model and train controller
from train_model.train_model_manager import TrainModelManager
from train_controller.train_controller_manager import TrainControllerManager

class Launcher(QMainWindow):
    def __init__(self):

        # API for CTC and Track Controller
        self.ctc_track_controller_api = CTCTrackControllerAPI()

        # API for Track Controller and Track Model
        self.track_controller_track_model_api = TrackControllerTrackModelAPI()

        # API for Track Model and Train Model
        self.track_model_train_model_api = TrackModelTrainModelAPI()

        # API for Train Model and Train Controller
        self.train_model_train_controller_api = TrainModelTrainControllerAPI()

        # TODO: CTC, track controllers, and track model need to change to use the APIs -- See train_model.py and train_controller.py for examples
        # Link APIs together
        # self.ctc = CTC(self.ctc_track_controller_api)
        self.track_controller = Track_Controller(self.ctc_track_controller_api, self.track_controller_track_model_api)
        # self.track_controller_hw = TrackControllerHW(self.ctc_track_controller_api, self.track_controller_track_model_api)
        # self.track_model = TrackModel(self.track_controller_track_model_api, self.track_model_train_model_api)
        self.train_model_manager = TrainModelManager(self.train_model_train_controller_api, self.track_model_train_model_api)
        self.train_controller_manager = TrainControllerManager(self.train_model_train_controller_api)

        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setObjectName("self")
        self.resize(339, 579)
        # self.centralwidget = QtWidgets.QWidget(MainWindow)
        # self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 341, 51))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.CTC_launch = QtWidgets.QPushButton(self)
        self.CTC_launch.setGeometry(QtCore.QRect(10, 60, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.CTC_launch.setFont(font)
        self.CTC_launch.setObjectName("CTC_launch")
        self.track_controller_sw_launch = QtWidgets.QPushButton(self)
        self.track_controller_sw_launch.setGeometry(QtCore.QRect(10, 130, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.track_controller_sw_launch.setFont(font)
        self.track_controller_sw_launch.setObjectName("track_controller_sw_launch")
        self.track_controller_hw_launch = QtWidgets.QPushButton(self)
        self.track_controller_hw_launch.setGeometry(QtCore.QRect(10, 200, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.track_controller_hw_launch.setFont(font)
        self.track_controller_hw_launch.setObjectName("track_controller_hw_launch")
        self.track_model_launch = QtWidgets.QPushButton(self)
        self.track_model_launch.setGeometry(QtCore.QRect(10, 270, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.track_model_launch.setFont(font)
        self.track_model_launch.setObjectName("track_model_launch")
        self.train_model_launch = QtWidgets.QPushButton(self)
        # Disable button until train is selected
        # self.train_model_launch.setStyleSheet(
        #     "QPushButton:disabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(90, 90, 90);\n"
        #     "}\n"
        #     "QPushButton:enabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(255, 255, 255);\n"
        #     "}\n"
        #     # "\n"
        #     # ""
        # )
        self.train_model_launch.setGeometry(QtCore.QRect(10, 340, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.train_model_launch.setFont(font)
        self.train_model_launch.setObjectName("train_model_launch")
        self.train_controller_launch = QtWidgets.QPushButton(self)
        # Disable button until train is selected
        # self.train_controller_launch.setStyleSheet(
        #     "QPushButton:disabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(90, 90, 90);\n"
        #     "}\n"
        #     "QPushButton:enabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(255, 255, 255);\n"
        #     "}\n"
        #     # "\n"
        #     # ""
        # )
        self.train_controller_launch.setGeometry(QtCore.QRect(10, 460, 321, 61))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.train_controller_launch.setFont(font)
        self.train_controller_launch.setObjectName("train_controller_launch")
        self.train_model_select = QtWidgets.QComboBox(self)
        # Disable button until train is selected
        # self.train_model_select.setStyleSheet(
        #     "QPushButton:disabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(255, 255, 255);\n"
        #     "}\n"
        #     "QPushButton:enabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(255, 255, 255);\n"
        #     "}\n"
        #     # "\n"
        #     # ""
        # )
        self.train_model_select.setGeometry(QtCore.QRect(10, 400, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.train_model_select.setFont(font)
        self.train_model_select.setObjectName("train_model_select")
        self.train_controller_select = QtWidgets.QComboBox(self)
        # Disable button until train is selected
        # self.train_controller_select.setStyleSheet(
        #     "QPushButton:disabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(255, 255, 255);\n"
        #     "}\n"
        #     "QPushButton:enabled {\n"
        #     "background-color: rgb(63, 63, 63);\n"
        #     "color: rgb(255, 255, 255);\n"
        #     "}\n"
        #     # "\n"
        #     # ""
        # )
        self.train_controller_select.setGeometry(QtCore.QRect(10, 520, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.train_controller_select.setFont(font)
        self.train_controller_select.setObjectName("train_controller_select")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        # TODO: CTC, track controllers, and track model need to add a launch function -- See below for examples
        # TODO: Also reference the manager functions in train_model_manager.py and train_controller_manager.py
        # TODO: You will need to edit how your UI is built to be launched from the launcher -- See Train_Model_UI.py
        # Launch UI on Click
        # self.CTC_launch.clicked.connect(self.launch_ctc)
        self.track_controller_sw_launch.clicked.connect(self.launch_track_controller_sw)
        # self.track_controller_hw_launch.clicked.connect(self.launch_track_controller_hw)
        # self.track_model_launch.clicked.connect(self.launch_track_model)
        self.train_model_launch.clicked.connect(self.launch_train_model)
        self.train_controller_launch.clicked.connect(self.launch_train_controller)

        # Run Timer
        self._handler()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Launcher"))
        self.label.setText(_translate("MainWindow", "Planes Over Trains #5"))
        self.CTC_launch.setText(_translate("MainWindow", "CTC"))
        self.track_controller_sw_launch.setText(_translate("MainWindow", "Track Controller - SW"))
        self.track_controller_hw_launch.setText(_translate("MainWindow", "Track Controller - HW"))
        self.track_model_launch.setText(_translate("MainWindow", "Track Model"))
        self.train_model_launch.setText(_translate("MainWindow", "Train Model"))
        self.train_controller_launch.setText(_translate("MainWindow", "Train Controller"))

    def _handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)  # refreshes every time period
        self.timer.timeout.connect(self._update)
        self.timer.start()

    def _update(self):

        print("Updating Launcher")

        # Comment this out until train is dispatched
        # Disable Button for Train Model if no train selected
        # if self.train_model_select.currentText() == "":
        #     self.train_model_launch.setEnabled(False)
        # else:
        #     self.train_model_launch.setEnabled(True)

        # Disable Button for Train Model if no train selected
        # if self.train_controller_select.currentText() == "":
        #     self.train_controller_launch.setEnabled(False)
        # else:
        #     self.train_controller_launch.setEnabled(True)

    def get_train_models(self):
        self.train_model_select.clear()
        self.train_model_select.addItems(
            [f'train #{id + 1}' for id in self.train_model_manager.get_ids()]
        )
    def get_train_controllers(self):
        self.train_controller_select.clear()
        self.train_controller_select.addItems(
            [f'train #{id + 1}' for id in self.train_controller_manager.get_ids()]
        )

    '''
    # Uncomment this section when you have implemented a launch function for your module
    def launch_ctc(self):
        self.ctc.launch_ui()
        
    def launch_track_controller_hw(self):
        self.track_controller_hw.launch_ui()
        
    def launch_track_model(self):
        self.track_model.launch_ui()
    '''

    def launch_track_controller_sw(self):
        self.track_controller.launch_ui()

    def launch_train_model(self):
        # comment out this line until train is dispatched
        # id = int(self.train_model_select.currentText()[-1]) - 1
        # self.train_model_manager.launch_ui(id)
        self.train_model_manager.launch_ui(0)
    def launch_train_controller(self):
        # comment out this line until train is dispatched
        # id = int(self.train_model_select.currentText()[-1]) - 1
        # self.train_model_manager.launch_ui(id)
        self.train_controller_manager.launch_ui(0)

class ComboBox(QtWidgets.QComboBox):
    popupAboutToBeShown = QtCore.pyqtSignal()

    def showPopup(self):
        self.popupAboutToBeShown.emit()
        super(ComboBox, self).showPopup()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    e = Launcher()
    sys.exit(app.exec_())