# -*- coding: utf-8 -*-
import traceback

# Form implementation generated from reading ui file 'Track_Controller_HW_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import serial
from PyQt5 import QtCore, QtGui, QtWidgets
from track_controller_hw.File_Parser import File_Parser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from track_controller_hw.Track_Controller_UI_Testbench import Ui_Test_Bench
from track_controller_hw.track_controller_hw import Track_Controller_HW
from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.track_controller_track_model_api import TrackControllerTrackModelAPI

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


class Ui_track_controller_mainwindow(QMainWindow):

    def __init__(self, track_controller_hw: Track_Controller_HW) -> None:
        super().__init__()
        self.track_controller_hw = track_controller_hw
        self._previous = ""
        self._send_bits = ""
        self.setupUi()
        self.show()
        self.change = True

    def set_previous_show(self, s: str):
        self._previous = s

    def get_previous_show(self) -> str:
        return self._previous


    def get_send_bits(self) -> str:
        return self._send_bits

    def set_send_bits(self, l: str):
        self._send_bits = l

    def open_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Test_Bench(self.track_controller_hw)
        self.ui.setupUi(self.window)
        self.window.show()

    def browse_files(self):
        print("Test")
        browse = QFileDialog.getOpenFileName(self.load_plc_button)
        print(browse[0])
        data = File_Parser(browse[0])
        self.track_controller_hw.set_plc_logic(data)
        self.track_controller_hw.set_plc_set(True)
        print("Test End")

    def setupUi(self):
        self.setObjectName("track_controller_mainwindow")
        self.resize(500, 538)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(0, 0, 711, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title_label.setFont(font)
        self.title_label.setAutoFillBackground(False)
        self.title_label.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                       "border: 3px solid black;")
        self.sys_time_label = QtWidgets.QLabel(self.centralwidget)
        self.sys_time_label.setGeometry(QtCore.QRect(400, 8, 83, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sys_time_label.setFont(font)
        self.sys_time_label.setStyleSheet("border: 1px solid black;\n"
                                          "background-color: rgb(255, 255, 255);")
        self.sys_time_label.setObjectName("sys_time_label")
        self.title_label.setObjectName("title_label")

        self.select_output = QtWidgets.QListWidget(self.centralwidget)
        self.select_output.setGeometry(QtCore.QRect(260, 200, 231, 231))
        self.select_output.setObjectName("select_output")
        item = QtWidgets.QListWidgetItem()
        self.select_output.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.select_output.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.select_output.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.select_output.addItem(item)
        self.wayside_select = QtWidgets.QComboBox(self.centralwidget)
        self.wayside_select.setGeometry(QtCore.QRect(60, 130, 231, 25))
        self.wayside_select.setEditable(True)
        self.wayside_select.setObjectName("wayside_select")
        self.wayside_select.addItem("")
        self.wayside_select.addItem("")
        self.load_plc_label = QtWidgets.QLabel(self.centralwidget)
        self.load_plc_label.setGeometry(QtCore.QRect(300, 60, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.load_plc_label.setFont(font)
        self.load_plc_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                          "border: 1px solid black;\n"
                                          "")
        self.load_plc_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.load_plc_label.setObjectName("load_plc_label")
        self.selected_output = QtWidgets.QLineEdit(self.centralwidget)
        self.selected_output.setGeometry(QtCore.QRect(60, 490, 211, 25))
        self.selected_output.setText("")
        self.selected_output.setObjectName("selected_output")
        self.show_ard_light = QtWidgets.QPushButton(self, clicked=lambda: self.toggle_light())
        self.show_ard_light.setGeometry(QtCore.QRect(500, 490, 93, 28))
        self.show_ard_light.setObjectName("show_ard")
        self.show_ard_light.setText("Change Light")
        self.show_ard_switch = QtWidgets.QPushButton(self, clicked=lambda: self.toggle_switch())
        self.show_ard_switch.setGeometry(QtCore.QRect(600, 490, 93, 28))
        self.show_ard_switch.setObjectName("show_ard")
        self.show_ard_switch.setText("Change Switch")

        self.plc_output = QtWidgets.QListWidget(self.centralwidget)
        self.plc_output.setGeometry(QtCore.QRect(520, 190, 191, 261))
        self.plc_output.setObjectName("plc_output")
        self.plc_output_label = QtWidgets.QLabel(self.centralwidget)
        self.plc_output_label.setGeometry(QtCore.QRect(520, 150, 198, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.plc_output_label.setFont(font)
        self.plc_output_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "border: 1px solid black;\n"
                                            "")
        self.plc_output_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.plc_output_label.setObjectName("plc_output_label")
        self.load_plc_button = QtWidgets.QPushButton(self,
                                                     clicked=lambda: self.browse_files())
        self.load_plc_button.setGeometry(QtCore.QRect(400, 60, 93, 28))
        self.load_plc_button.setObjectName("load_plc_button")
        self.Select_wayside_label = QtWidgets.QLabel(self.centralwidget)
        self.Select_wayside_label.setGeometry(QtCore.QRect(60, 100, 231, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Select_wayside_label.setFont(font)
        self.Select_wayside_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                "border: 1px solid black;\n"
                                                "")
        self.Select_wayside_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Select_wayside_label.setObjectName("Select_wayside_label")
        self.select_output_label = QtWidgets.QLabel(self.centralwidget)
        self.select_output_label.setGeometry(QtCore.QRect(260, 170, 198, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.select_output_label.setFont(font)
        self.select_output_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "border: 1px solid black;\n"
                                               "")
        self.select_output_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.select_output_label.setObjectName("select_output_label")
        self.selected_output_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_output_label.setGeometry(QtCore.QRect(60, 460, 198, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.selected_output_label.setFont(font)
        self.selected_output_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                 "border: 1px solid black;\n"
                                                 "")
        self.selected_output_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.selected_output_label.setObjectName("selected_output_label")
        self.occupancy_display = QtWidgets.QListWidget(self.centralwidget)
        self.occupancy_display.setGeometry(QtCore.QRect(10, 200, 231, 231))
        self.occupancy_display.setObjectName("occupancy_display")
        self.occupancy_label = QtWidgets.QLabel(self.centralwidget)
        self.occupancy_label.setGeometry(QtCore.QRect(10, 170, 221, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.occupancy_label.setFont(font)
        self.occupancy_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                           "border: 1px solid black;\n"
                                           "")
        self.occupancy_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.occupancy_label.setObjectName("occupancy_label")

        self.title_label.raise_()

        self.select_output.raise_()
        self.wayside_select.raise_()

        self.load_plc_label.raise_()
        self.selected_output.raise_()
        self.plc_output.raise_()
        self.plc_output_label.raise_()
        self.load_plc_button.raise_()
        self.Select_wayside_label.raise_()
        self.select_output_label.raise_()
        self.selected_output_label.raise_()
        self.occupancy_display.raise_()
        self.occupancy_label.raise_()
        self.sys_time_label.raise_()
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.select_output.clear()
        self._handler()

        for i in self.track_controller_hw.get_switch_list():
            self.select_output.addItem(i)

        for i in self.track_controller_hw.get_lights_list():
            if i not in self.track_controller_hw.get_switch_list():
                self.select_output.addItem(i)

        self.wayside_select.clear()

        self.wayside_select.addItem("Green")

    def update(self):
        _translate = QtCore.QCoreApplication.translate
        temp_time = self.track_controller_hw.get_time()
        hr = str(temp_time.hour)
        minute = str(temp_time.minute)
        sec = str(temp_time.second)
        if len(hr) == 1:
            hr = "0" + hr
        if len(minute) == 1:
            minute = "0" + minute
        if len(sec) == 1:
            sec = "0" + sec
        temp_timestr = hr + ":" + minute + ":" + sec
        self.sys_time_label.setText(_translate("self", temp_timestr))

        self.plc_output.clear()


        self.occupancy_display.clear()
        try:
            for i in self.track_controller_hw.get_occupied():
                if i is not None:
                    self.occupancy_display.addItem(str(i))
        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()

        self.plc_output.setVisible(False)
        self.plc_output_label.setVisible(False)
        if not self.track_controller_hw.get_automatic():
            self.show_ard_light.setVisible(True)
            self.show_ard_switch.setVisible(True)

        else:
            self.show_ard_light.setVisible(False)
            self.show_ard_switch.setVisible(False)

        try:
            block_number = self.select_output.currentItem().text()
            self.selected_output.setText(block_number)
            if self.get_previous_show() != block_number:
                self.set_previous_show(block_number)
                self.track_controller_hw.select_block(block_number)
        except Exception as e:
            print("An error occurred:")
            traceback.print_exc()


    def _handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)  # refreshes every time period
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("track_controller_mainwindow", "Track Controller Hardware"))
        self.title_label.setText(_translate("track_controller_mainwindow", "Wayside Controller - Hardware"))

        __sortingEnabled = self.select_output.isSortingEnabled()
        self.select_output.setSortingEnabled(False)
        item = self.select_output.item(0)
        item.setText(_translate("track_controller_mainwindow", "Light B-C11"))
        item = self.select_output.item(1)
        item.setText(_translate("track_controller_mainwindow", "Light  B-A5"))
        item = self.select_output.item(2)
        item.setText(_translate("track_controller_mainwindow", "Light B-B6"))
        item = self.select_output.item(3)
        item.setText(_translate("track_controller_mainwindow", "Switch B -A5/B6/C11"))
        self.select_output.setSortingEnabled(__sortingEnabled)
        self.wayside_select.setItemText(0, _translate("track_controller_mainwindow", "Blue 1"))
        self.wayside_select.setItemText(1, _translate("track_controller_mainwindow", "Blue 2"))
        self.load_plc_label.setText(_translate("track_controller_mainwindow", "PLC"))
        self.plc_output_label.setText(_translate("track_controller_mainwindow", "PLC Output"))
        self.load_plc_button.setText(_translate("track_controller_mainwindow", "Load PLC"))
        self.Select_wayside_label.setText(_translate("track_controller_mainwindow", "Wayside Controller/Line"))
        self.select_output_label.setText(_translate("track_controller_mainwindow", "Select Output"))
        self.selected_output_label.setText(_translate("track_controller_mainwindow", "Selected Output"))
        self.occupancy_label.setText(_translate("track_controller_mainwindow", "Blocks Occupied"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    e = Ui_track_controller_mainwindow(Track_Controller_HW(CTCTrackControllerAPI, TrackControllerTrackModelAPI))
    sys.exit(app.exec_())
