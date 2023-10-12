# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ryanr\Documents\SchoolStuff\Fall2023\ECE_1140\Track_Controller_TB.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import uic
from track_controller import Track_Controller
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
import time
import sys


class Ui_TrackController_Testbench(object):

    def __init__(self, track_controller: Track_Controller):
        super().__init__()
        self.track_controller = track_controller
    def setupUi(self, Frame):
        Frame.setObjectName("Testbench")
        Frame.resize(478, 634)
        self.testbench_label = QtWidgets.QLabel(Frame)
        self.testbench_label.setGeometry(QtCore.QRect(0, 0, 478, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.testbench_label.setFont(font)
        self.testbench_label.setAutoFillBackground(False)
        self.testbench_label.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border: 3px solid black;")
        self.testbench_label.setAlignment(QtCore.Qt.AlignCenter)
        self.testbench_label.setObjectName("testbench_label")
        self.track_model_label = QtWidgets.QLabel(Frame)
        self.track_model_label.setGeometry(QtCore.QRect(0, 54, 478, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.track_model_label.setFont(font)
        self.track_model_label.setAutoFillBackground(False)
        self.track_model_label.setStyleSheet("")
        self.track_model_label.setAlignment(QtCore.Qt.AlignCenter)
        self.track_model_label.setObjectName("track_model_label")
        self.block_information_label = QtWidgets.QLabel(Frame)
        self.block_information_label.setGeometry(QtCore.QRect(2, 96, 477, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.block_information_label.setFont(font)
        self.block_information_label.setAlignment(QtCore.Qt.AlignCenter)
        self.block_information_label.setObjectName("block_information_label")
        self.block_comboBox = QtWidgets.QComboBox(Frame)
        self.block_comboBox.setGeometry(QtCore.QRect(12, 130, 170, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.block_comboBox.setFont(font)
        self.block_comboBox.setObjectName("block_comboBox")
        self.block_comboBox.addItem("")
        self.block_comboBox.addItem("")
        self.block_comboBox.addItem("")
        self.block_comboBox.addItem("")
        self.block_comboBox.addItem("")
        self.block_comboBox.addItem("B6")
        self.block_comboBox.addItem("B7")
        self.block_comboBox.addItem("B8")
        self.block_comboBox.addItem("B9")
        self.block_comboBox.addItem("B10")
        self.block_comboBox.addItem("C11")
        self.block_comboBox.addItem("C12")
        self.block_comboBox.addItem("C13")
        self.block_comboBox.addItem("C14")
        self.block_comboBox.addItem("C15")
        self.toggle_occupancy_button = QtWidgets.QPushButton(Frame, clicked=lambda:self.track_controller.set_occupancy(self.block_comboBox.currentText(), not bool(self.track_controller.get_occupancy(self.block_comboBox.currentText()))))
        self.toggle_occupancy_button.setGeometry(QtCore.QRect(12, 168, 170, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.toggle_occupancy_button.setFont(font)
        self.toggle_occupancy_button.setObjectName("toggle_occupancy_button")
        self.speed_limit_spinBox = QtWidgets.QSpinBox(Frame, valueChanged=lambda: self.track_controller.set_speed_limit(self.block_comboBox.currentText(), self.speed_limit_spinBox.value()))
        self.speed_limit_spinBox.setGeometry(QtCore.QRect(130, 208, 52, 28))
        self.speed_limit_spinBox.setObjectName("speed_limit_spinBox")
        self.speed_limit_label = QtWidgets.QLabel(Frame)
        self.speed_limit_label.setGeometry(QtCore.QRect(12, 214, 79, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.speed_limit_label.setFont(font)
        self.speed_limit_label.setObjectName("speed_limit_label")
        self.failures = QtWidgets.QTextBrowser(Frame)
        self.failures.setGeometry(QtCore.QRect(256, 145, 174, 141))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.failures.setFont(font)
        self.failures.setFrameShape(QtWidgets.QFrame.Box)
        self.failures.setFrameShadow(QtWidgets.QFrame.Plain)
        self.failures.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.failures.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.failures.setObjectName("failures")
        self.failure_label = QtWidgets.QLabel(Frame)
        self.failure_label.setGeometry(QtCore.QRect(214, 125, 256, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.failure_label.setFont(font)
        self.failure_label.setAlignment(QtCore.Qt.AlignCenter)
        self.failure_label.setObjectName("failure_label")
        self.change_switch_position_button = QtWidgets.QPushButton(Frame, clicked=lambda:self.track_controller.set_switch(self.switch_comboBox.currentText(), not self.track_controller.get_switch(self.switch_comboBox.currentText())))
        self.change_switch_position_button.setGeometry(QtCore.QRect(12, 356, 170, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.change_switch_position_button.setFont(font)
        self.change_switch_position_button.setObjectName("change_switch_position_button")
        self.switch_comboBox = QtWidgets.QComboBox(Frame)
        self.switch_comboBox.setGeometry(QtCore.QRect(12, 318, 170, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.switch_comboBox.setFont(font)
        self.switch_comboBox.setObjectName("switch_comboBox")
        self.switch_comboBox.addItem("")
        self.switch_position_label = QtWidgets.QLabel(Frame)
        self.switch_position_label.setGeometry(QtCore.QRect(12, 294, 170, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.switch_position_label.setFont(font)
        self.switch_position_label.setAlignment(QtCore.Qt.AlignCenter)
        self.switch_position_label.setObjectName("switch_position_label")
        self.light_color_label = QtWidgets.QLabel(Frame)
        self.light_color_label.setGeometry(QtCore.QRect(259, 294, 170, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.light_color_label.setFont(font)
        self.light_color_label.setAlignment(QtCore.Qt.AlignCenter)
        self.light_color_label.setObjectName("light_color_label")
        self.light_red_button = QtWidgets.QPushButton(Frame, clicked=lambda:self.track_controller.set_lights(self.light_color_comboBox.currentText(), 1))
        self.light_red_button.setGeometry(QtCore.QRect(219, 356, 117, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.light_red_button.setFont(font)
        self.light_red_button.setObjectName("light_red_button")
        self.light_color_comboBox = QtWidgets.QComboBox(Frame)
        self.light_color_comboBox.setGeometry(QtCore.QRect(259, 318, 170, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.light_color_comboBox.setFont(font)
        self.light_color_comboBox.setObjectName("light_color_comboBox")
        self.light_color_comboBox.addItem("")
        self.light_color_comboBox.addItem("")
        self.light_color_comboBox.addItem("")
        self.light_green_button = QtWidgets.QPushButton(Frame, clicked=lambda:self.track_controller.set_lights(self.light_color_comboBox.currentText(), 0))
        self.light_green_button.setGeometry(QtCore.QRect(350, 356, 117, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.light_green_button.setFont(font)
        self.light_green_button.setObjectName("light_green_button")
        self.ctc_officel_label = QtWidgets.QLabel(Frame)
        self.ctc_officel_label.setGeometry(QtCore.QRect(0, 402, 478, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.ctc_officel_label.setFont(font)
        self.ctc_officel_label.setAutoFillBackground(False)
        self.ctc_officel_label.setStyleSheet("")
        self.ctc_officel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ctc_officel_label.setObjectName("ctc_officel_label")
        self.track_status_label = QtWidgets.QLabel(Frame)
        self.track_status_label.setGeometry(QtCore.QRect(23, 550, 170, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.track_status_label.setFont(font)
        self.track_status_label.setAlignment(QtCore.Qt.AlignCenter)
        self.track_status_label.setObjectName("track_status_label")
        self.track_status_button = QtWidgets.QPushButton(Frame, clicked=lambda:self.track_controller.set_occupancy(self.track_status_comboBox.currentText(), not self.track_controller.get_occupancy(self.track_status_comboBox.currentText())))
        self.track_status_button.setGeometry(QtCore.QRect(289, 546, 170, 28))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.track_status_button.setFont(font)
        self.track_status_button.setObjectName("track_status_button")
        self.track_status_comboBox = QtWidgets.QComboBox(Frame)
        self.track_status_comboBox.setGeometry(QtCore.QRect(170, 545, 100, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.track_status_comboBox.setFont(font)
        self.track_status_comboBox.setObjectName("track_status_comboBox")
        self.track_status_comboBox.addItem("")
        self.track_status_comboBox.addItem("")
        self.track_status_comboBox.addItem("")
        self.track_status_comboBox.addItem("")
        self.track_status_comboBox.addItem("")
        self.track_status_comboBox.addItem("B6")
        self.track_status_comboBox.addItem("B7")
        self.track_status_comboBox.addItem("B8")
        self.track_status_comboBox.addItem("B9")
        self.track_status_comboBox.addItem("B10")
        self.track_status_comboBox.addItem("C11")
        self.track_status_comboBox.addItem("C12")
        self.track_status_comboBox.addItem("C13")
        self.track_status_comboBox.addItem("C14")
        self.track_status_comboBox.addItem("C15")
        self.suggested_speed_label = QtWidgets.QLabel(Frame)
        self.suggested_speed_label.setGeometry(QtCore.QRect(102, 456, 127, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.suggested_speed_label.setFont(font)
        self.suggested_speed_label.setObjectName("suggested_speed_label")
        self.suggested_speed_spinBox = QtWidgets.QSpinBox(Frame)
        self.suggested_speed_spinBox.setGeometry(QtCore.QRect(268, 454, 52, 28))
        self.suggested_speed_spinBox.setObjectName("suggested_speed_spinBox")
        self.authority_label = QtWidgets.QLabel(Frame)
        self.authority_label.setGeometry(QtCore.QRect(130, 502, 79, 16))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.authority_label.setFont(font)
        self.authority_label.setObjectName("authority_label")
        self.authority_spinBox = QtWidgets.QSpinBox(Frame)
        self.authority_spinBox.setGeometry(QtCore.QRect(269, 496, 52, 28))
        self.authority_spinBox.setObjectName("authority_spinBox")
        self.broken_rail_checkBox = QtWidgets.QCheckBox(Frame, stateChanged=lambda:self.track_controller.set_occupancy(self.block_comboBox.currentText(), self.broken_rail_checkBox.isChecked()))
        self.broken_rail_checkBox.setGeometry(QtCore.QRect(292, 158, 107, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.broken_rail_checkBox.setFont(font)
        self.broken_rail_checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.broken_rail_checkBox.setShortcut("")
        self.broken_rail_checkBox.setObjectName("broken_rail_checkBox")
        self.circuit_checkBox = QtWidgets.QCheckBox(Frame, stateChanged=lambda:self.track_controller.set_occupancy(self.block_comboBox.currentText(), self.circuit_checkBox.isChecked()))
        self.circuit_checkBox.setGeometry(QtCore.QRect(314, 184, 65, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.circuit_checkBox.setFont(font)
        self.circuit_checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.circuit_checkBox.setShortcut("")
        self.circuit_checkBox.setObjectName("circuit_checkBox")
        self.power_checkBox = QtWidgets.QCheckBox(Frame, stateChanged=lambda:self.track_controller.set_occupancy(self.block_comboBox.currentText(), self.power_checkBox.isChecked()))
        self.power_checkBox.setGeometry(QtCore.QRect(314, 210, 66, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.power_checkBox.setFont(font)
        self.power_checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.power_checkBox.setShortcut("")
        self.power_checkBox.setObjectName("power_checkBox")
        self.brake_checkBox = QtWidgets.QCheckBox(Frame, stateChanged=lambda:self.track_controller.set_occupancy(self.block_comboBox.currentText(), self.brake_checkBox.isChecked()))
        self.brake_checkBox.setGeometry(QtCore.QRect(312, 236, 63, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.brake_checkBox.setFont(font)
        self.brake_checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.brake_checkBox.setShortcut("")
        self.brake_checkBox.setObjectName("brake_checkBox")
        self.train_engine_checkBox = QtWidgets.QCheckBox(Frame, stateChanged=lambda:self.track_controller.set_occupancy(self.block_comboBox.currentText(), self.train_engine_checkBox.isChecked()))
        self.train_engine_checkBox.setGeometry(QtCore.QRect(292, 260, 107, 22))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.train_engine_checkBox.setFont(font)
        self.train_engine_checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.train_engine_checkBox.setShortcut("")
        self.train_engine_checkBox.setObjectName("train_engine_checkBox")
        self.failures.raise_()
        self.testbench_label.raise_()
        self.track_model_label.raise_()
        self.block_information_label.raise_()
        self.block_comboBox.raise_()
        self.toggle_occupancy_button.raise_()
        self.speed_limit_spinBox.raise_()
        self.speed_limit_label.raise_()
        self.failure_label.raise_()
        self.change_switch_position_button.raise_()
        self.switch_comboBox.raise_()
        self.switch_position_label.raise_()
        self.light_color_label.raise_()
        self.light_red_button.raise_()
        self.light_color_comboBox.raise_()
        self.light_green_button.raise_()
        self.ctc_officel_label.raise_()
        self.track_status_label.raise_()
        self.track_status_button.raise_()
        self.track_status_comboBox.raise_()
        self.suggested_speed_label.raise_()
        self.suggested_speed_spinBox.raise_()
        self.authority_label.raise_()
        self.authority_spinBox.raise_()
        self.broken_rail_checkBox.raise_()
        self.circuit_checkBox.raise_()
        self.power_checkBox.raise_()
        self.brake_checkBox.raise_()
        self.train_engine_checkBox.raise_()

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)


    def retranslateUi(self, Frame):
        _translate = QtCore.QCoreApplication.translate
        Frame.setWindowTitle(_translate("Frame", "Testbench"))
        self.testbench_label.setText(_translate("Frame", "Track Controller"))
        self.track_model_label.setText(_translate("Frame", "Track Model"))
        self.block_information_label.setText(_translate("Frame", "Block Information"))
        self.block_comboBox.setItemText(0, _translate("Frame", "A1"))
        self.block_comboBox.setItemText(1, _translate("Frame", "A2"))
        self.block_comboBox.setItemText(2, _translate("Frame", "A3"))
        self.block_comboBox.setItemText(3, _translate("Frame", "A4"))
        self.block_comboBox.setItemText(4, _translate("Frame", "A5"))
        self.block_comboBox.setItemText(5, _translate("Frame", "B6"))
        self.block_comboBox.setItemText(6, _translate("Frame", "B7"))
        self.block_comboBox.setItemText(7, _translate("Frame", "B8"))
        self.block_comboBox.setItemText(8, _translate("Frame", "B9"))
        self.block_comboBox.setItemText(9, _translate("Frame", "B10"))
        self.block_comboBox.setItemText(10, _translate("Frame", "C11"))
        self.block_comboBox.setItemText(11, _translate("Frame", "C12"))
        self.block_comboBox.setItemText(12, _translate("Frame", "C13"))
        self.block_comboBox.setItemText(13, _translate("Frame", "C14"))
        self.block_comboBox.setItemText(14, _translate("Frame", "C15"))
        self.toggle_occupancy_button.setText(_translate("Frame", "Change Occupancy"))
        self.speed_limit_label.setText(_translate("Frame", "Speed Limit"))
        self.failure_label.setText(_translate("Frame", "Failures"))
        self.change_switch_position_button.setText(_translate("Frame", "Change Position"))
        self.switch_comboBox.setItemText(0, _translate("Frame", "BC-A"))
        self.switch_position_label.setText(_translate("Frame", "Switch Position"))
        self.light_color_label.setText(_translate("Frame", "Light Color"))
        self.light_red_button.setText(_translate("Frame", "Red"))
        self.light_color_comboBox.setItemText(0, _translate("Frame", "A5"))
        self.light_color_comboBox.setItemText(1, _translate("Frame", "B6"))
        self.light_color_comboBox.setItemText(2, _translate("Frame", "C11"))
        self.light_green_button.setText(_translate("Frame", "Green"))
        self.ctc_officel_label.setText(_translate("Frame", "CTC Office"))
        self.track_status_label.setText(_translate("Frame", "Track Status"))
        self.track_status_button.setText(_translate("Frame", "Toggle Maintenance"))
        self.track_status_comboBox.setItemText(0, _translate("Frame", "A1"))
        self.track_status_comboBox.setItemText(1, _translate("Frame", "A2"))
        self.track_status_comboBox.setItemText(2, _translate("Frame", "A3"))
        self.track_status_comboBox.setItemText(3, _translate("Frame", "A4"))
        self.track_status_comboBox.setItemText(4, _translate("Frame", "A5"))
        self.track_status_comboBox.setItemText(5, _translate("Frame", "B6"))
        self.track_status_comboBox.setItemText(6, _translate("Frame", "B7"))
        self.track_status_comboBox.setItemText(7, _translate("Frame", "B8"))
        self.track_status_comboBox.setItemText(8, _translate("Frame", "B9"))
        self.track_status_comboBox.setItemText(9, _translate("Frame", "B10"))
        self.track_status_comboBox.setItemText(10, _translate("Frame", "C11"))
        self.track_status_comboBox.setItemText(11, _translate("Frame", "C12"))
        self.track_status_comboBox.setItemText(12, _translate("Frame", "C13"))
        self.track_status_comboBox.setItemText(13, _translate("Frame", "C14"))
        self.track_status_comboBox.setItemText(14, _translate("Frame", "C15"))
        self.suggested_speed_label.setText(_translate("Frame", "Suggested Speed"))
        self.authority_label.setText(_translate("Frame", "Authority"))
        self.broken_rail_checkBox.setText(_translate("Frame", "Broken Rail"))
        self.circuit_checkBox.setText(_translate("Frame", "Circuit"))
        self.power_checkBox.setText(_translate("Frame", "Power"))
        self.brake_checkBox.setText(_translate("Frame", "Brake"))
        self.train_engine_checkBox.setText(_translate("Frame", "Train Engine"))

    def update(self):
        self.speed_limit_spinBox.setValue(self.track_controller.get_speed_limit(self.block_comboBox.currentText()))

        self.track_controller.set_suggested_speed(self.suggested_speed_spinBox.value())
        self.track_controller.set_authority(self.authority_spinBox.value())
        self.track_controller.set_test_speed_limit(self.speed_limit_spinBox.value())
        self.track_controller.set_speed_limit(self.block_comboBox.currentText(), self.track_controller.get_test_speed_limit())
    def _handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)  # refreshes every time period
        self.timer.timeout.connect(self.update)
        self.timer.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Frame = QtWidgets.QFrame()
    tc = Track_Controller
    ui = Ui_TrackController_Testbench(tc)
    ui.setupUi(Frame)
    Frame.show()
    sys.exit(app.exec_())
