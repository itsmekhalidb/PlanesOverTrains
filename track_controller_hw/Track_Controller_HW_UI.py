# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Track_Controller_HW_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import serial
from PyQt5 import uic
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

from PlanesOverTrains.track_controller_hw.Track_Controller_UI_Testbench import Ui_Test_Bench
from PlanesOverTrains.track_controller_hw.track_controller_hw import Track_Controller_HW

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
import sys


class Ui_track_controller_mainwindow(object):

    def __init__(self, track_controller_hw: Track_Controller_HW):
        super().__init__()
        self.track_controller_hw = track_controller_hw
        self._light = False
        self._switch = False
        self._command = False
        self._ard = serial.Serial(port='COM5', baudrate=9600, timeout=.1)

    def set_light_show(self, l: bool):
        self._light = l

    def get_light_show(self) -> bool:
        return self._light

    def set_switch_show(self, l: bool):
        self._switch = l

    def get_switch_show(self) -> bool:
        return self._switch

    def set_command_show(self, l: bool):
        self._command = l

    def get_command_show(self) -> bool:
        return self._command

    def open_window(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Test_Bench(self.track_controller_hw)  # Pass the TrainModel instance to the new UI
        self.ui.setupUi(self.window)
        self.window.show()

    def get_ard(self):
        return self._ard

    def setupUi(self, track_controller_mainwindow_ui):
        track_controller_mainwindow_ui.setObjectName("track_controller_mainwindow")
        track_controller_mainwindow_ui.resize(727, 538)
        self.centralwidget = QtWidgets.QWidget(track_controller_mainwindow_ui)
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
        self.title_label.setObjectName("title_label")
        self.system_speed_spnbx = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.system_speed_spnbx.setGeometry(QtCore.QRect(634, 14, 62, 22))
        self.system_speed_spnbx.setObjectName("system_speed_spnbx")
        self.system_speed_label = QtWidgets.QLabel(self.centralwidget)
        self.system_speed_label.setGeometry(QtCore.QRect(498, 10, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.system_speed_label.setFont(font)
        self.system_speed_label.setAutoFillBackground(False)
        self.system_speed_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                              "border: 1px solid black;")
        self.system_speed_label.setObjectName("system_speed_label")
        self.manual_mode_check = QtWidgets.QCheckBox(self.centralwidget)
        self.manual_mode_check.setEnabled(True)
        self.manual_mode_check.setGeometry(QtCore.QRect(210, 62, 14, 15))
        self.manual_mode_check.setObjectName("manual_mode_check")
        self.ebrake_fail_on = QtWidgets.QLabel(self.centralwidget)
        self.ebrake_fail_on.setEnabled(True)
        self.ebrake_fail_on.setGeometry(QtCore.QRect(176, 60, 25, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ebrake_fail_on.setFont(font)
        self.ebrake_fail_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                                          "background-color: rgb(0, 170, 0);")
        self.ebrake_fail_on.setAlignment(QtCore.Qt.AlignCenter)
        self.ebrake_fail_on.setObjectName("ebrake_fail_on")
        self.manual_mode_label = QtWidgets.QLabel(self.centralwidget)
        self.manual_mode_label.setGeometry(QtCore.QRect(8, 56, 198, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.manual_mode_label.setFont(font)
        self.manual_mode_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "border: 1px solid black;\n"
                                             "")
        self.manual_mode_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.manual_mode_label.setObjectName("manual_mode_label")
        self.manual_mode_off = QtWidgets.QLabel(self.centralwidget)
        self.manual_mode_off.setEnabled(True)
        self.manual_mode_off.setGeometry(QtCore.QRect(150, 60, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.manual_mode_off.setFont(font)
        self.manual_mode_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "background-color: rgb(170, 0, 0);")
        self.manual_mode_off.setAlignment(QtCore.Qt.AlignCenter)
        self.manual_mode_off.setObjectName("manual_mode_off")
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
        self.wayside_select.setGeometry(QtCore.QRect(260, 130, 231, 25))
        self.wayside_select.setEditable(True)
        self.wayside_select.setObjectName("wayside_select")
        self.wayside_select.addItem("")
        self.wayside_select.addItem("")
        self.manual_mode_on = QtWidgets.QLabel(self.centralwidget)
        self.manual_mode_on.setEnabled(True)
        self.manual_mode_on.setGeometry(QtCore.QRect(180, 60, 25, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.manual_mode_on.setFont(font)
        self.manual_mode_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                                          "background-color: rgb(0, 170, 0);")
        self.manual_mode_on.setAlignment(QtCore.Qt.AlignCenter)
        self.manual_mode_on.setObjectName("manual_mode_on")
        self.load_plc_label = QtWidgets.QLabel(self.centralwidget)
        self.load_plc_label.setGeometry(QtCore.QRect(500, 60, 91, 31))
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
        self.selected_output.setGeometry(QtCore.QRect(260, 490, 211, 25))
        self.selected_output.setText("")
        self.selected_output.setObjectName("selected_output")
        self.show_ard = QtWidgets.QPushButton(track_controller_mainwindow_ui, clicked=lambda: self.toggle())
        self.show_ard.setGeometry(QtCore.QRect(500, 490, 93, 28))
        self.show_ard.setObjectName("show_ard")
        self.show_ard.setText("Change")
        self.command_spin = QtWidgets.QSpinBox(track_controller_mainwindow_ui,
                                               valueChanged=lambda: self.track_controller_hw.set_commanded_speed(
                                                   self.command_spin.value()))
        self.command_spin.setGeometry(QtCore.QRect(170, 490, 42, 22))
        self.command_spin.setObjectName("command_spin")
        self.command_label = QtWidgets.QLabel(self.centralwidget)
        self.command_label.setGeometry(QtCore.QRect(110, 460, 121, 27))
        self.command_label.setObjectName("command_label")
        self.command_label.setText("Commanded")
        self.command_label.setFont(font)
        self.command_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                         "border: 1px solid black;\n"
                                         "")
        self.command_drop = QtWidgets.QComboBox(self.centralwidget)
        self.command_drop.setGeometry(QtCore.QRect(100, 490, 61, 25))
        self.command_drop.setObjectName("command_drop")
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
        self.load_plc_button = QtWidgets.QPushButton(self.centralwidget)
        self.load_plc_button.setGeometry(QtCore.QRect(600, 60, 93, 28))
        self.load_plc_button.setObjectName("load_plc_button")
        self.Select_wayside_label = QtWidgets.QLabel(self.centralwidget)
        self.Select_wayside_label.setGeometry(QtCore.QRect(260, 100, 231, 27))
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
        self.selected_output_label.setGeometry(QtCore.QRect(260, 460, 198, 27))
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
        self.testbench_button = QtWidgets.QPushButton(track_controller_mainwindow_ui,
                                                      clicked=lambda: self.open_window())
        self.testbench_button.setGeometry(QtCore.QRect(10, 480, 81, 31))
        self.testbench_button.setObjectName("testbench_button")
        self.title_label.raise_()
        self.system_speed_label.raise_()
        self.system_speed_spnbx.raise_()
        self.manual_mode_check.raise_()
        self.ebrake_fail_on.raise_()
        self.manual_mode_label.raise_()
        self.manual_mode_off.raise_()
        self.select_output.raise_()
        self.wayside_select.raise_()
        self.manual_mode_on.raise_()
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
        self.testbench_button.raise_()
        track_controller_mainwindow_ui.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(track_controller_mainwindow_ui)
        self.statusbar.setObjectName("statusbar")
        track_controller_mainwindow_ui.setStatusBar(self.statusbar)

        self.retranslateUi(track_controller_mainwindow_ui)
        QtCore.QMetaObject.connectSlotsByName(track_controller_mainwindow_ui)

        self.select_output.clear()
        self._handler()

        for x in self.track_controller_hw.get_switch_list():
            self.select_output.addItem(x)

        item = QListWidgetItem("Select Output Above")

        for x in self.track_controller_hw.get_light_list():
            self.select_output.addItem(x)

        for x in self.track_controller_hw.get_blue_track():
            self.command_drop.addItem(x)

        for i in self.track_controller_hw.get_blue_track():
            if self.track_controller_hw.get_occupancy(i) == 1:
                item = str(i) + " " + str(self.track_controller_hw.get_speed_limit(i)) + " mi/hr"
                self.occupancy_display.addItem(item)

        self.select_output.addItem("Commanded Speed")
        self.wayside_select.clear()

        self.wayside_select.addItem("Blue")


        self.select_output.addItem(item)
        self.select_output.setCurrentItem(item)

    def update(self):
        _translate = QtCore.QCoreApplication.translate

        self.plc_output.clear()

        self.system_speed_label.setVisible(False)
        self.system_speed_spnbx.setVisible(False)

        self.occupancy_display.clear()
        self.occupancy_display.addItems(self.track_controller_hw.get_occupied_blocks())

        self.track_controller_hw.set_automatic(not self.manual_mode_check.checkState())

        self.command_drop.setVisible(False)

        if not self.track_controller_hw.get_automatic():
            self.show_ard.setVisible(True)
            self.command_label.setVisible(True)
            self.command_spin.setVisible(True)
            #self.command_drop.setVisible(True)
        else:
            self.show_ard.setVisible(False)
            self.command_label.setVisible(False)
            self.command_spin.setVisible(False)

        self.load_plc_button.setVisible(not bool(self.manual_mode_check.checkState()))
        # label visibility
        self.manual_mode_off.setVisible(not bool(self.manual_mode_check.checkState()))
        self.manual_mode_on.setVisible(bool(self.manual_mode_check.checkState()))

        if self.track_controller_hw.get_automatic():
            self.PLC()

        try:
            if self.select_output.currentItem().text() == "Hello":
                print("Value is None")
            else:
                value = self.select_output.currentItem().text()
                self.selected_output.setText(value)
                type_output = self.selected_output.text().split(" ")

                if type_output[0] == "Light":
                    if not self.get_light_show():
                        self.send_lights()
                        self.set_light_show(True)
                        self.set_switch_show(False)
                        self.set_command_show(False)
                elif type_output[0] == "Switch":
                    if not self.get_switch_show():
                        self.send_switch()
                        self.set_light_show(False)
                        self.set_switch_show(True)
                        self.set_command_show(False)
                elif type_output[0] == "Commanded":
                    if not self.get_command_show():
                        self.send_command(True)
                        self.set_light_show(False)
                        self.set_switch_show(False)
                        self.set_command_show(True)
        except:
            print("Non Value")

    # try:
    # self.track_controller_hw.set_commanded_speed(
    #     self.track_controller_hw.get_suggested_speed() - self.track_controller_hw.get_speed_limit('B-A1'))
    # except:
    #    print("None")

    def toggle(self):
        type_output = self.selected_output.text().split(" ")
        if type_output[0] == "Light":
            if self.track_controller_hw.get_lights(self.selected_output.text()) == 0:
                self.change_light(1, self.selected_output.text())
                self.send_lights()
            elif self.track_controller_hw.get_lights(self.selected_output.text()) == 1:
                self.change_light(0, self.selected_output.text())
                self.send_lights()
        elif type_output[0] == "Switch":
            self.change_switch(self.selected_output.text())
            self.send_switch()
        elif type_output[0] == "Commanded":
            self.send_command(False)

    def change_light(self, i: int, light: str):
        type_output = self.selected_output.text().split(" ")
        if i == 0:
            self.track_controller_hw.set_lights(0, light)
        elif i == 1:
            self.track_controller_hw.set_lights(1, light)
        elif i == 2:
            self.track_controller_hw.set_lights(2, light)

    def change_switch(self, switch: str):
        if self.track_controller_hw.get_switch(switch) == 0:
            self.track_controller_hw.set_switch(1, switch)
        elif self.track_controller_hw.get_switch(switch) == 1:
            self.track_controller_hw.set_switch(0, switch)

    def send_lights(self):
        type_output = self.selected_output.text().split(" ")
        value = self.select_output.currentItem().text()
        if type_output[0] == "Light":
            print("Light")
            send = "1001" + str(self.track_controller_hw.get_lights(value)) + str(type_output[1])
            self.get_ard().write(send.encode('utf-8'))

    def send_command(self, value: bool):
        type_output = self.selected_output.text().split(" ")
        if type_output[0] == "Commanded":
            print("Commanded")
            if value:
                com = self.track_controller_hw.get_suggested_speed() - self.track_controller_hw.get_speed_limit('B-A1')
            else:
                com = self.track_controller_hw.get_commanded_speed()
            send = "11000" + str(com)
            self.get_ard().write(send.encode('utf-8'))

    def send_switch(self):
        type_output = self.selected_output.text().split(" ")
        value = self.select_output.currentItem().text()
        if type_output[0] == "Switch":
            print("Switch")
            if self.track_controller_hw.get_switch(value) == 0:
                send = "10100" + str(type_output[1]) + " => C"
                self.get_ard().write(send.encode('utf-8'))
            elif self.track_controller_hw.get_switch(value) == 1:
                send = "10100" + str(type_output[1]) + " => A"
                self.get_ard().write(send.encode('utf-8'))

    def _handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)  # refreshes every time period
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def retranslateUi(self, track_controller_mainwindow):
        _translate = QtCore.QCoreApplication.translate
        track_controller_mainwindow.setWindowTitle(_translate("track_controller_mainwindow", "MainWindow"))
        self.title_label.setText(_translate("track_controller_mainwindow", "Wayside Controller - Hardware"))
        self.system_speed_label.setText(_translate("track_controller_mainwindow", " System Speed"))
        self.manual_mode_check.setText(_translate("track_controller_mainwindow", "Manual Mode"))
        self.ebrake_fail_on.setText(_translate("track_controller_mainwindow", "ON"))
        self.manual_mode_label.setText(_translate("track_controller_mainwindow", "Manual Mode"))
        self.manual_mode_off.setText(_translate("track_controller_mainwindow", "OFF"))
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
        self.manual_mode_on.setText(_translate("track_controller_mainwindow", "ON"))
        self.load_plc_label.setText(_translate("track_controller_mainwindow", "PLC BLUE"))
        self.plc_output_label.setText(_translate("track_controller_mainwindow", "PLC Output"))
        self.load_plc_button.setText(_translate("track_controller_mainwindow", "Load PLC"))
        self.Select_wayside_label.setText(_translate("track_controller_mainwindow", "Wayside Controller/Line"))
        self.select_output_label.setText(_translate("track_controller_mainwindow", "Select Output"))
        self.selected_output_label.setText(_translate("track_controller_mainwindow", "Selected Output"))
        self.occupancy_label.setText(_translate("track_controller_mainwindow", "Blocks Occupied- Limit"))
        self.testbench_button.setText(_translate("track_controller_mainwindow", "Testbench"))

    def PLC(self):
        self.track_controller_hw.set_commanded_speed(
            min(self.track_controller_hw.get_suggested_speed(), self.track_controller_hw.get_speed_limit('B-A1')))

        self.sect_A_occ = bool(self.track_controller_hw.get_occupancy('B-A1') or self.track_controller_hw.get_occupancy(
            'B-A2') or self.track_controller_hw.get_occupancy('B-A3') or self.track_controller_hw.get_occupancy(
            'B-A4') or self.track_controller_hw.get_occupancy('B-A5'))
        self.sect_B_occ = bool(self.track_controller_hw.get_occupancy('B-B6') or self.track_controller_hw.get_occupancy(
            'B-B7') or self.track_controller_hw.get_occupancy('B-B8') or self.track_controller_hw.get_occupancy(
            'B-B9') or self.track_controller_hw.get_occupancy('B-B10'))
        self.sect_C_occ = bool(
            self.track_controller_hw.get_occupancy('B-C11') or self.track_controller_hw.get_occupancy(
                'B-C12') or self.track_controller_hw.get_occupancy('B-C13') or self.track_controller_hw.get_occupancy(
                'B-C14') or self.track_controller_hw.get_occupancy('B-C15'))
        if self.sect_A_occ:
            self.plc_output.addItem("Train detected in section A")
            self.track_controller_hw.set_lights(0, 'Light B-A5')
            self.track_controller_hw.set_lights(1, 'Light B-B6')
            self.track_controller_hw.set_lights(1, 'Light C-C11')
            if self.sect_B_occ:
                self.plc_output_output.addItem("Train detected in section B")
                self.track_controller_hw.set_lights(1, 'Light B-A5', )
                self.track_controller_hw.set_lights(1, 'Light B-B6')
                self.track_controller_hw.set_lights(1, 'Light B-C11')
                self.track_controller_hw.set_switch(1, 'Switch BC-A')
                self.plc_output.addItem("Stopping traffic from track section B")
                self.plc_output.addItem("Switching to track section C")
            elif self.sect_C_occ:
                self.plc_output.addItem("Train detected in section C")
                self.track_controller_hw.set_lights(0, 'Light B-A5')
                self.track_controller_hw.set_lights(0, 'Light B-B6')
                self.track_controller_hw.set_lights(1, 'Light B-C11')
                self.track_controller_hw.set_switch(0, 'Switch BC-A')
                self.plc_output.addItem("Stopping traffic from track section C")
                self.plc_output.addItem("Switching to track section B")
            else:
                self.plc_output.addItem("Stopping traffic from track sections B and C")
                self.plc_output.addItem("Switching to track section B")
        elif self.sect_B_occ:
            self.plc_output.addItem("Train detected in section B")
            self.track_controller_hw.set_lights(0, 'Light B-A5')
            self.track_controller_hw.set_lights(1, 'Light B-B6')
            self.track_controller_hw.set_lights(0, 'Light B-C11')
            self.track_controller_hw.set_switch(1, 'Light BC-A')
            self.plc_output.addItem("Stopping traffic from track sections A and C")
            self.plc_output.addItem("Switching to track section B")
        elif self.sect_C_occ:
            self.plc_output.addItem("Train detected in section C")
            self.track_controller_hw.set_lights(1, 'Light B-A5')
            self.track_controller_hw.set_lights(1, 'Light B-B6')
            self.track_controller_hw.set_lights(0, 'Light B-C11')
            self.track_controller_hw.set_switch(0, 'Switch BC-A')
            self.plc_output.addItem("Stopping traffic from track sections A and B")
            self.plc_output.addItem("Switching to track section C")
        else:
            self.plc_output.addItem("No trains on the track")
            self.track_controller_hw.set_lights(0, 'Light B-A5')
            self.track_controller_hw.set_lights(0, 'Light B-B6')
            self.track_controller_hw.set_lights(0, 'Light B-C11')


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    track_controller_mainwindow = QtWidgets.QMainWindow()
    track_controller_hw = Track_Controller_HW()
    ui = Ui_track_controller_mainwindow(track_controller_hw)
    ui.setupUi(track_controller_mainwindow)
    track_controller_mainwindow.show()
    sys.exit(app.exec_())
