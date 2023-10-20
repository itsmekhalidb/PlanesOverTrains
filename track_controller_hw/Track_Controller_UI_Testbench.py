# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Track_Controller_HW_UI_Testbench.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer

from PlanesOverTrains.track_controller_hw.track_controller_hw import Track_Controller_HW


class Ui_Test_Bench(object):

    def __init__(self, track_controller_hw: Track_Controller_HW):
        super().__init__()
        self.track_controller_hw = track_controller_hw

    def setupUi(self, test_bench):
        test_bench.setObjectName("MainWindow")
        test_bench.resize(613, 509)
        self.centralwidget = QtWidgets.QWidget(test_bench)
        self.centralwidget.setObjectName("centralwidget")
        self.maintence_mode_button = QtWidgets.QPushButton(test_bench,clicked=lambda: self.change_occupancy_maintenance_mode())
        self.maintence_mode_button.setGeometry(QtCore.QRect(350, 460, 221, 28))
        self.maintence_mode_button.setObjectName("maintence_mode_button")
        self.title_label_2 = QtWidgets.QLabel(self.centralwidget)
        self.title_label_2.setGeometry(QtCore.QRect(0, 0, 611, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title_label_2.setFont(font)
        self.title_label_2.setAutoFillBackground(False)
        self.title_label_2.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                         "border: 3px solid black;")
        self.title_label_2.setObjectName("title_label_2")
        self.light_red_button = QtWidgets.QPushButton(test_bench, clicked=lambda: self.change_light(0))
        self.light_red_button.setGeometry(QtCore.QRect(10, 290, 93, 28))
        self.light_red_button.setObjectName("light_red_button")
        self.broken_label_on = QtWidgets.QLabel(self.centralwidget)
        self.broken_label_on.setEnabled(True)
        self.broken_label_on.setGeometry(QtCore.QRect(540, 108, 25, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.broken_label_on.setFont(font)
        self.broken_label_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                                           "background-color: rgb(0, 170, 0);")
        self.broken_label_on.setAlignment(QtCore.Qt.AlignCenter)
        self.broken_label_on.setObjectName("broken_label_on")
        self.ebrake_fail_on = QtWidgets.QLabel(self.centralwidget)
        self.ebrake_fail_on.setEnabled(True)
        self.ebrake_fail_on.setGeometry(QtCore.QRect(536, 108, 25, 17))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ebrake_fail_on.setFont(font)
        self.ebrake_fail_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                                          "background-color: rgb(0, 170, 0);")
        self.ebrake_fail_on.setAlignment(QtCore.Qt.AlignCenter)
        self.ebrake_fail_on.setObjectName("ebrake_fail_on")
        self.power_failure_on = QtWidgets.QLabel(self.centralwidget)
        self.power_failure_on.setEnabled(True)
        self.power_failure_on.setGeometry(QtCore.QRect(540, 170, 25, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.power_failure_on.setFont(font)
        self.power_failure_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "background-color: rgb(0, 170, 0);")
        self.power_failure_on.setAlignment(QtCore.Qt.AlignCenter)
        self.power_failure_on.setObjectName("power_failure_on")
        self.train_engine_failure_label = QtWidgets.QLabel(self.centralwidget)
        self.train_engine_failure_label.setGeometry(QtCore.QRect(325, 196, 241, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.train_engine_failure_label.setFont(font)
        self.train_engine_failure_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                      "border: 1px solid black;\n"
                                                      "")
        self.train_engine_failure_label.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.train_engine_failure_label.setObjectName("train_engine_failure_label")
        self.block_drop = QtWidgets.QComboBox(self.centralwidget)
        self.block_drop.setGeometry(QtCore.QRect(10, 100, 231, 25))
        self.block_drop.setEditable(True)
        self.block_drop.setObjectName("block_drop")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.block_drop.addItem("")
        self.light_select_drop = QtWidgets.QComboBox(self.centralwidget)
        self.light_select_drop.setGeometry(QtCore.QRect(10, 260, 231, 25))
        self.light_select_drop.setEditable(True)
        self.light_select_drop.setObjectName("light_select_drop")
        self.light_select_drop.addItem("")
        self.light_select_drop.addItem("")
        self.light_select_drop.addItem("")
        self.light_select_drop.addItem("")
        self.light_select_drop.setItemText(3, "")
        self.broken_rail_label = QtWidgets.QLabel(self.centralwidget)
        self.broken_rail_label.setGeometry(QtCore.QRect(325, 104, 241, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.broken_rail_label.setFont(font)
        self.broken_rail_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "border: 1px solid black;\n"
                                             "")
        self.broken_rail_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.broken_rail_label.setObjectName("broken_rail_label")
        self.circuit_failure_label = QtWidgets.QLabel(self.centralwidget)
        self.circuit_failure_label.setGeometry(QtCore.QRect(325, 136, 241, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.circuit_failure_label.setFont(font)
        self.circuit_failure_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                 "border: 1px solid black;\n"
                                                 "")
        self.circuit_failure_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.circuit_failure_label.setObjectName("circuit_failure_label")
        self.train_engine_failure_off = QtWidgets.QLabel(self.centralwidget)
        self.train_engine_failure_off.setEnabled(True)
        self.train_engine_failure_off.setGeometry(QtCore.QRect(510, 200, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.train_engine_failure_off.setFont(font)
        self.train_engine_failure_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                    "background-color: rgb(170, 0, 0);")
        self.train_engine_failure_off.setAlignment(QtCore.Qt.AlignCenter)
        self.train_engine_failure_off.setObjectName("train_engine_failure_off")
        self.track_status_drop = QtWidgets.QComboBox(self.centralwidget)
        self.track_status_drop.setGeometry(QtCore.QRect(240, 460, 91, 25))
        self.track_status_drop.setEditable(True)
        self.track_status_drop.setObjectName("track_status_drop")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.track_status_drop.addItem("")
        self.authoriy_label = QtWidgets.QLabel(self.centralwidget)
        self.authoriy_label.setGeometry(QtCore.QRect(20, 380, 198, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.authoriy_label.setFont(font)
        self.authoriy_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                          "border: 1px solid black;\n"
                                          "")
        self.authoriy_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.authoriy_label.setObjectName("authoriy_label")
        self.switch_drop = QtWidgets.QComboBox(self.centralwidget)
        self.switch_drop.setGeometry(QtCore.QRect(10, 180, 231, 25))
        self.switch_drop.setEditable(True)
        self.switch_drop.setObjectName("switch_drop")
        self.switch_drop.addItem("")
        self.authority_input = QtWidgets.QLineEdit(self.centralwidget)
        self.authority_input.setGeometry(QtCore.QRect(240, 380, 211, 25))
        self.authority_input.setText("")
        self.authority_input.setObjectName("authority_input")
        self.suggested_speed_label = QtWidgets.QLabel(self.centralwidget)
        self.suggested_speed_label.setGeometry(QtCore.QRect(20, 420, 198, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.suggested_speed_label.setFont(font)
        self.suggested_speed_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                                 "border: 1px solid black;\n"
                                                 "")
        self.suggested_speed_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.suggested_speed_label.setObjectName("suggested_speed_label")
        self.broken_label_off = QtWidgets.QLabel(self.centralwidget)
        self.broken_label_off.setEnabled(True)
        self.broken_label_off.setGeometry(QtCore.QRect(510, 108, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.broken_label_off.setFont(font)
        self.broken_label_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                                            "background-color: rgb(170, 0, 0);")
        self.broken_label_off.setAlignment(QtCore.Qt.AlignCenter)
        self.broken_label_off.setObjectName("broken_label_off")
        self.power_failure_label = QtWidgets.QLabel(self.centralwidget)
        self.power_failure_label.setGeometry(QtCore.QRect(325, 166, 241, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.power_failure_label.setFont(font)
        self.power_failure_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                               "border: 1px solid black;\n"
                                               "")
        self.power_failure_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.power_failure_label.setObjectName("power_failure_label")
        self.train_engine_failure_check = QtWidgets.QCheckBox(test_bench, stateChanged=lambda:self.change_occupancy())
        self.train_engine_failure_check.setEnabled(True)
        self.train_engine_failure_check.setGeometry(QtCore.QRect(570, 200, 14, 15))
        self.train_engine_failure_check.setObjectName("train_engine_failure_check")
        self.ctc_label = QtWidgets.QLabel(self.centralwidget)
        self.ctc_label.setGeometry(QtCore.QRect(10, 340, 571, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ctc_label.setFont(font)
        self.ctc_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                     "border: 1px solid black;\n"
                                     "")
        self.ctc_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.ctc_label.setObjectName("ctc_label")
        self.super_green_light_button = QtWidgets.QPushButton(test_bench, clicked=lambda: self.change_light(2))
        self.super_green_light_button.setGeometry(QtCore.QRect(210, 290, 101, 28))
        self.super_green_light_button.setObjectName("super_green_light_button")
        self.selected_output_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_output_label.setGeometry(QtCore.QRect(340, 260, 198, 27))
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
        self.broken_rail_check = QtWidgets.QCheckBox(test_bench, stateChanged=lambda:self.change_occupancy())
        self.broken_rail_check.setEnabled(True)
        self.broken_rail_check.setGeometry(QtCore.QRect(570, 110, 14, 15))
        self.broken_rail_check.setObjectName("broken_rail_check")
        self.light_green_button = QtWidgets.QPushButton(test_bench, clicked=lambda: self.change_light(1))
        self.light_green_button.setGeometry(QtCore.QRect(110, 290, 93, 28))
        self.light_green_button.setObjectName("light_green_button")
        self.circuit_failure_on = QtWidgets.QLabel(self.centralwidget)
        self.circuit_failure_on.setEnabled(True)
        self.circuit_failure_on.setGeometry(QtCore.QRect(540, 140, 25, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.circuit_failure_on.setFont(font)
        self.circuit_failure_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                                              "background-color: rgb(0, 170, 0);")
        self.circuit_failure_on.setAlignment(QtCore.Qt.AlignCenter)
        self.circuit_failure_on.setObjectName("circuit_failure_on")
        self.change_switch_button = QtWidgets.QPushButton(test_bench, clicked=lambda: self.change_switch())
        self.change_switch_button.setGeometry(QtCore.QRect(10, 210, 131, 31))
        self.change_switch_button.setObjectName("change_switch_button")
        self.selected_output = QtWidgets.QLineEdit(self.centralwidget)
        self.selected_output.setGeometry(QtCore.QRect(340, 290, 211, 25))
        self.selected_output.setText("")
        self.selected_output.setObjectName("selected_output")
        self.suggested_soeed_input = QtWidgets.QLineEdit(self.centralwidget)
        self.suggested_soeed_input.setGeometry(QtCore.QRect(240, 420, 211, 25))
        self.suggested_soeed_input.setText("")
        self.suggested_soeed_input.setObjectName("suggested_soeed_input")
        self.change_occupancy_button = QtWidgets.QPushButton(test_bench, clicked=lambda: self.change_occupancy())
        self.change_occupancy_button.setGeometry(QtCore.QRect(10, 130, 161, 31))
        self.change_occupancy_button.setObjectName("change_occupancy_button")
        self.circuit_failure_check = QtWidgets.QCheckBox(test_bench, stateChanged=lambda:self.change_occupancy())
        self.circuit_failure_check.setEnabled(True)
        self.circuit_failure_check.setGeometry(QtCore.QRect(570, 142, 14, 15))
        self.circuit_failure_check.setObjectName("circuit_failure_check")
        self.track_status_label = QtWidgets.QLabel(self.centralwidget)
        self.track_status_label.setGeometry(QtCore.QRect(20, 460, 198, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.track_status_label.setFont(font)
        self.track_status_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                              "border: 1px solid black;\n"
                                              "")
        self.track_status_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.track_status_label.setObjectName("track_status_label")
        self.circuit_failure_off = QtWidgets.QLabel(self.centralwidget)
        self.circuit_failure_off.setEnabled(True)
        self.circuit_failure_off.setGeometry(QtCore.QRect(510, 140, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.circuit_failure_off.setFont(font)
        self.circuit_failure_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                                               "background-color: rgb(170, 0, 0);")
        self.circuit_failure_off.setAlignment(QtCore.Qt.AlignCenter)
        self.circuit_failure_off.setObjectName("circuit_failure_off")
        self.train_engine_failure_on = QtWidgets.QLabel(self.centralwidget)
        self.train_engine_failure_on.setEnabled(True)
        self.train_engine_failure_on.setGeometry(QtCore.QRect(540, 200, 25, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.train_engine_failure_on.setFont(font)
        self.train_engine_failure_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                                                   "background-color: rgb(0, 170, 0);")
        self.train_engine_failure_on.setAlignment(QtCore.Qt.AlignCenter)
        self.train_engine_failure_on.setObjectName("train_engine_failure_on")
        self.track_model_label = QtWidgets.QLabel(self.centralwidget)
        self.track_model_label.setGeometry(QtCore.QRect(10, 60, 571, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.track_model_label.setFont(font)
        self.track_model_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                             "border: 1px solid black;\n"
                                             "")
        self.track_model_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.track_model_label.setObjectName("track_model_label")
        self.power_failure_check = QtWidgets.QCheckBox(test_bench, stateChanged=lambda:self.change_occupancy())
        self.power_failure_check.setEnabled(True)
        self.power_failure_check.setGeometry(QtCore.QRect(570, 172, 14, 15))
        self.power_failure_check.setObjectName("power_failure_check")
        self.power_failure_off = QtWidgets.QLabel(self.centralwidget)
        self.power_failure_off.setEnabled(True)
        self.power_failure_off.setGeometry(QtCore.QRect(510, 170, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.power_failure_off.setFont(font)
        self.power_failure_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                                             "background-color: rgb(170, 0, 0);")
        self.power_failure_off.setAlignment(QtCore.Qt.AlignCenter)
        self.power_failure_off.setObjectName("power_failure_off")
        test_bench.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(test_bench)
        self.statusbar.setObjectName("statusbar")
        test_bench.setStatusBar(self.statusbar)

        self.broken_rail_label.lower()
        self.power_failure_label.lower()

        self.retranslateUi(test_bench)
        QtCore.QMetaObject.connectSlotsByName(test_bench)
        self.ebrake_fail_on.setVisible(False)
        self.block_drop.clear()
        self.switch_drop.clear()
        self.light_select_drop.clear()
        self.track_status_drop.clear()

        for x in self.track_controller_hw.get_switch_list():
            self.switch_drop.addItem(x)

        for x in self.track_controller_hw.get_light_list():
            self.light_select_drop.addItem(x)

        for i in self.track_controller_hw.get_blue_track():
            self.block_drop.addItem(i)
            self.track_status_drop.addItem(i)

        self._handler()

        self.selected_output.setText("50")
        self.authority_input.setText("0")
        self.suggested_soeed_input.setText("0")
        self.super_green_light_button.setVisible(False)

    def _handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)  # refreshes every time period
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def change_light(self, i: int):
        if i == 0:
            self.track_controller_hw.set_lights(0, self.light_select_drop.currentText())
        elif i == 1:
            self.track_controller_hw.set_lights(1, self.light_select_drop.currentText())
        elif i == 2:
            self.track_controller_hw.set_lights(2, self.light_select_drop.currentText())

    def change_occupancy_maintenance_mode(self):
        if self.track_controller_hw.get_occupancy(self.track_status_drop.currentText()) == 0:
            self.track_controller_hw.set_occupancy(self.track_status_drop.currentText(), 1)
            print(self.block_drop.currentText() + "1")
        elif self.track_controller_hw.get_occupancy(self.track_status_drop.currentText()) == 1:
            self.track_controller_hw.set_occupancy(self.track_status_drop.currentText(), 0)


    def change_occupancy(self):
        if self.track_controller_hw.get_occupancy(self.block_drop.currentText()) == 0:
            self.track_controller_hw.set_occupancy(self.block_drop.currentText(), 1)
            print(self.block_drop.currentText() + "1")
        elif self.track_controller_hw.get_occupancy(self.block_drop.currentText()) == 1:
            self.track_controller_hw.set_occupancy(self.block_drop.currentText(), 0)

    def change_switch(self):
        if self.track_controller_hw.get_switch(self.switch_drop.currentText()) == 0:
            self.track_controller_hw.set_switch(1, self.switch_drop.currentText())
            print(self.switch_drop.currentText() + "1")
        elif self.track_controller_hw.get_switch(self.switch_drop.currentText()) == 1:
            self.track_controller_hw.set_switch(0, self.switch_drop.currentText())

    def update(self):
        self.authority_input.setVisible(False)
        self.authoriy_label.setVisible(False)

        self.broken_label_off.setVisible(not bool(self.broken_rail_check.checkState()))
        self.broken_label_on.setVisible(bool(self.broken_rail_check.checkState()))

        self.circuit_failure_off.setVisible(not bool(self.circuit_failure_check.checkState()))
        self.circuit_failure_on.setVisible(bool(self.circuit_failure_check.checkState()))

        self.power_failure_off.setVisible(not bool(self.power_failure_check.checkState()))
        self.power_failure_on.setVisible(bool(self.power_failure_check.checkState()))

        self.train_engine_failure_off.setVisible(not bool(self.train_engine_failure_check.checkState()))
        self.train_engine_failure_on.setVisible(bool(self.train_engine_failure_check.checkState()))

        try:
            self.track_controller_hw.set_suggested_speed(float(self.suggested_soeed_input.text()))
        except:
            print("No Value")

        try:
            self.track_controller_hw.set_test_speed_limit(float(self.selected_output.text()))
            self.track_controller_hw.set_authority(float(self.authority_input.text()))
            print("Value")
        except:
            print("No Value Yet")

        self.track_controller_hw.set_speed_limit(self.block_drop.currentText(),
                                              self.track_controller_hw.get_test_speed_limit())
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.maintence_mode_button.setText(_translate("MainWindow", "Toggle Maintance Mode"))
        self.title_label_2.setText(_translate("MainWindow", "Testbench"))
        self.light_red_button.setText(_translate("MainWindow", "Red"))
        self.broken_label_on.setText(_translate("MainWindow", "ON"))
        self.ebrake_fail_on.setText(_translate("MainWindow", "ON"))
        self.power_failure_on.setText(_translate("MainWindow", "ON"))
        self.train_engine_failure_label.setText(_translate("MainWindow", "Train Engine Failure"))
        self.block_drop.setItemText(0, _translate("MainWindow", "B-A1"))
        self.block_drop.setItemText(1, _translate("MainWindow", "B-A2"))
        self.block_drop.setItemText(2, _translate("MainWindow", "B-A3"))
        self.block_drop.setItemText(3, _translate("MainWindow", "B-A4"))
        self.block_drop.setItemText(4, _translate("MainWindow", "B-A5"))
        self.block_drop.setItemText(5, _translate("MainWindow", "B-B6"))
        self.block_drop.setItemText(6, _translate("MainWindow", "B-B7"))
        self.block_drop.setItemText(7, _translate("MainWindow", "B-B8"))
        self.block_drop.setItemText(8, _translate("MainWindow", "B-B9"))
        self.block_drop.setItemText(9, _translate("MainWindow", "B-B10"))
        self.block_drop.setItemText(10, _translate("MainWindow", "B-C11"))
        self.block_drop.setItemText(11, _translate("MainWindow", "B-C12"))
        self.block_drop.setItemText(12, _translate("MainWindow", "B-C13"))
        self.block_drop.setItemText(13, _translate("MainWindow", "B-C14"))
        self.block_drop.setItemText(14, _translate("MainWindow", "B-C15"))
        self.light_select_drop.setItemText(0, _translate("MainWindow", "B-A5"))
        self.light_select_drop.setItemText(1, _translate("MainWindow", "B-C11"))
        self.light_select_drop.setItemText(2, _translate("MainWindow", "B-B6"))
        self.broken_rail_label.setText(_translate("MainWindow", "Broken Rail"))
        self.circuit_failure_label.setText(_translate("MainWindow", "Circuit Failure"))
        self.train_engine_failure_off.setText(_translate("MainWindow", "OFF"))
        self.track_status_drop.setItemText(0, _translate("MainWindow", "B-A1"))
        self.track_status_drop.setItemText(1, _translate("MainWindow", "B-A2"))
        self.track_status_drop.setItemText(2, _translate("MainWindow", "B-A3"))
        self.track_status_drop.setItemText(3, _translate("MainWindow", "B-A4"))
        self.track_status_drop.setItemText(4, _translate("MainWindow", "B-A5"))
        self.track_status_drop.setItemText(5, _translate("MainWindow", "B-B6"))
        self.track_status_drop.setItemText(6, _translate("MainWindow", "B-B7"))
        self.track_status_drop.setItemText(7, _translate("MainWindow", "B-B8"))
        self.track_status_drop.setItemText(8, _translate("MainWindow", "B-B9"))
        self.track_status_drop.setItemText(9, _translate("MainWindow", "B-B10"))
        self.track_status_drop.setItemText(10, _translate("MainWindow", "B-C11"))
        self.track_status_drop.setItemText(11, _translate("MainWindow", "B-C12"))
        self.track_status_drop.setItemText(12, _translate("MainWindow", "B-C13"))
        self.track_status_drop.setItemText(13, _translate("MainWindow", "B-C14"))
        self.track_status_drop.setItemText(14, _translate("MainWindow", "B-C15"))
        self.authoriy_label.setText(_translate("MainWindow", "Authority"))
        self.switch_drop.setItemText(0, _translate("MainWindow", "B-A5"))
        self.suggested_speed_label.setText(_translate("MainWindow", "Suggested Speed"))
        self.broken_label_off.setText(_translate("MainWindow", "OFF"))
        self.power_failure_label.setText(_translate("MainWindow", "Power Failure"))
        self.train_engine_failure_check.setText(_translate("MainWindow", "Manual Mode"))
        self.ctc_label.setText(_translate("MainWindow", "CTC Office Inputs"))
        self.super_green_light_button.setText(_translate("MainWindow", "Super Green"))
        self.selected_output_label.setText(_translate("MainWindow", "Enter Speed Limit"))
        self.broken_rail_check.setText(_translate("MainWindow", "Manual Mode"))
        self.light_green_button.setText(_translate("MainWindow", "Green"))
        self.circuit_failure_on.setText(_translate("MainWindow", "ON"))
        self.change_switch_button.setText(_translate("MainWindow", "Change Switch"))
        self.change_occupancy_button.setText(_translate("MainWindow", "Change Occupancy"))
        self.circuit_failure_check.setText(_translate("MainWindow", "Manual Mode"))
        self.track_status_label.setText(_translate("MainWindow", "Track Status"))
        self.circuit_failure_off.setText(_translate("MainWindow", "OFF"))
        self.train_engine_failure_on.setText(_translate("MainWindow", "ON"))
        self.track_model_label.setText(_translate("MainWindow", "Track Model Inputs"))
        self.power_failure_check.setText(_translate("MainWindow", "Manual Mode"))
        self.power_failure_off.setText(_translate("MainWindow", "OFF"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    hw = Track_Controller_HW()
    ui = Ui_Test_Bench(hw)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
