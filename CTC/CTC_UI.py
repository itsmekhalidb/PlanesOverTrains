# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTC_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import typing
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTimeEdit, QApplication, QTableView, QHeaderView, QMainWindow, QWidget
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime, time
from CTC import CTC

from api.ctc_track_controller_api import CTCTrackControllerAPI

last_page = 0


class CTC_Main_UI(QMainWindow):

    def __init__(self, ctc : CTC) -> None:
        super().__init__()
        self.ctc = ctc
        self.setupUi()
        self.show()

    def setupUi(self):

        # create blue line test
        self.ctc.test_blue_line_CTC()

        # create pages
        self.setObjectName("MainWindow")
        self.resize(675, 690) # downsized from 980 x 690
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.view_switcher = QtWidgets.QStackedWidget(self.centralwidget)
        self.view_switcher.setGeometry(QtCore.QRect(0, 0, 675, 690))
        self.view_switcher.setObjectName("view_switcher")

        #main page
        self.train_view_page = QtWidgets.QWidget()
        self.train_view_page.setObjectName("train_view_page")
        self.switch_auto = QtWidgets.QPushButton(self.train_view_page)
        self.switch_auto.setGeometry(QtCore.QRect(10, 621, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.switch_auto.setFont(font)
        self.switch_auto.setObjectName("switch_auto")
        self.arrival_time = QtWidgets.QTimeEdit(self.train_view_page)
        self.arrival_time.setGeometry(QtCore.QRect(297, 430, 81, 22))
        self.arrival_time.setObjectName("arrival_time")
        self.arrival_time.setTime(QTime.currentTime().addSecs(2 * 3600))
        self.station_list = QtWidgets.QComboBox(self.train_view_page)
        self.station_list.setGeometry(QtCore.QRect(237, 370, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.station_list.setFont(font)
        self.station_list.setObjectName("station_list")
        self.station_list.addItem("Destination Station")
        for station_name in self.ctc.get_stations_names():
            self.station_list.addItem(station_name)
        self.confirm = QtWidgets.QPushButton(self.train_view_page)
        self.confirm.setGeometry(QtCore.QRect(297, 460, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm.setFont(font)
        self.confirm.setObjectName("confirm")
        not_qtime = time(self.arrival_time.time().hour(), self.arrival_time.time().minute(), self.arrival_time.time().second())
        mode = 0 # mode 0 is new train, 1 is adding a stop, 2 is editing the schedule
        train_index = -1 # -1 if creating new train, otherwise use train index
        self.confirm.clicked.connect(lambda:self.confirm_route(self.station_list.currentText(), not_qtime, mode, train_index))
        self.system_speed_label_3 = QtWidgets.QLabel(self.train_view_page)
        self.system_speed_label_3.setGeometry(QtCore.QRect(501, 10, 169, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.system_speed_label_3.setFont(font)
        self.system_speed_label_3.setAutoFillBackground(False)
        self.system_speed_label_3.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.system_speed_label_3.setObjectName("system_speed_label_3")
        self.testbench_button = QtWidgets.QPushButton(self.train_view_page)
        self.testbench_button.setGeometry(QtCore.QRect(315, 10, 81, 31))
        self.testbench_button.setObjectName("testbench_button")
        self.testbench_button.clicked.connect(self.open_testbench)
        self.system_speed_spnbx_3 = QtWidgets.QDoubleSpinBox(self.train_view_page)
        self.system_speed_spnbx_3.setGeometry(QtCore.QRect(605, 14, 62, 22))
        self.system_speed_spnbx_3.setObjectName("system_speed_spnbx_3")
        self.header = QtWidgets.QLabel(self.train_view_page)
        self.header.setGeometry(QtCore.QRect(0, 0, 676, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.header.setFont(font)
        self.header.setAutoFillBackground(False)
        self.header.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border: 3px solid black;")
        self.header.setObjectName("header")
        self.arrival_time_label = QtWidgets.QTextEdit(self.train_view_page)
        self.arrival_time_label.setGeometry(QtCore.QRect(287, 410, 101, 41))
        self.arrival_time_label.setObjectName("arrival_time_label")
        self.sys_time_label_3 = QtWidgets.QLabel(self.train_view_page)
        self.sys_time_label_3.setGeometry(QtCore.QRect(405, 10, 83, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sys_time_label_3.setFont(font)
        self.sys_time_label_3.setStyleSheet("border: 1px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.sys_time_label_3.setObjectName("sys_time_label_3")
        self.train_list_2 = QtWidgets.QTableView(self.train_view_page)
        self.train_list_2.setGeometry(QtCore.QRect(0, 50, 675, 271))
        self.train_list_2.setObjectName("train_list_2")
        self.train_list_2_data = QStandardItemModel()
        self.train_list_2_data.setHorizontalHeaderItem(0, QStandardItem("Train Number"))
        self.train_list_2_data.setHorizontalHeaderItem(1, QStandardItem("Departure Time"))
        self.train_list_2_data.setHorizontalHeaderItem(2, QStandardItem("Arrival Time"))
        self.train_list_2_data.setHorizontalHeaderItem(3, QStandardItem("Destination Station"))
        self.train_list_2_data.setHorizontalHeaderItem(4, QStandardItem("Current Authority"))
        self.train_list_2_data.setHorizontalHeaderItem(5, QStandardItem("Suggested Speed"))
        self.train_list_2_data.setHorizontalHeaderItem(6, QStandardItem("Current Speed"))
        self.train_list_2.setModel(self.train_list_2_data)
        header = self.train_list_2.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Automatically adjust column size
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        # data = [ # code to add data
        #     ["1", "08:00", "10:30", "East Liberty", "890 m", "89 mi/hr", "50 mi/hr"]
        #     # Add more rows as needed
        # ]

        # for row_index, row_data in enumerate(data):
        #     for column_index, cell_data in enumerate(row_data):
        #         item = QStandardItem(str(cell_data))
        #         self.train_list_2_data.setItem(row_index, column_index, item)

        self.occupied_blocks = QtWidgets.QScrollArea(self.train_view_page)
        self.occupied_blocks.setGeometry(QtCore.QRect(514, 460, 161, 191))
        self.occupied_blocks.setWidgetResizable(True)
        self.occupied_blocks.setObjectName("occupied_blocks")
        self.blocks_table_widget = QtWidgets.QWidget()
        self.blocks_table_widget.setGeometry(QtCore.QRect(0, 0, 159, 189))
        self.blocks_table_widget.setObjectName("blocks_table_widget")
        self.blocks_table = QtWidgets.QTableWidget(self.blocks_table_widget)
        self.blocks_table.setGeometry(QtCore.QRect(0, 0, 161, 192))
        self.blocks_table.setObjectName("blocks_table")
        self.blocks_table.setColumnCount(0)
        self.blocks_table.setRowCount(0)
        self.occupied_blocks.setWidget(self.blocks_table_widget)
        self.edit_schedule = QtWidgets.QPushButton(self.train_view_page)
        self.edit_schedule.setGeometry(QtCore.QRect(277, 400, 121, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_schedule.setFont(font)
        self.edit_schedule.setObjectName("edit_schedule")
        self.edit_schedule.hide()
        self.add_stop = QtWidgets.QPushButton(self.train_view_page)
        self.add_stop.setGeometry(QtCore.QRect(287, 360, 101, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_stop.setFont(font)
        self.add_stop.setObjectName("add_stop")
        self.add_stop.hide()
        self.label = QtWidgets.QLabel(self.train_view_page)
        self.label.setGeometry(QtCore.QRect(182, 611, 311, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.train_view_page)
        self.label_2.setGeometry(QtCore.QRect(248, 330, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.arrival_time_label.raise_()
        self.header.raise_()
        self.switch_auto.raise_()
        self.station_list.raise_()
        self.confirm.raise_()
        self.system_speed_label_3.raise_()
        self.testbench_button.raise_()
        self.arrival_time.raise_()
        self.system_speed_spnbx_3.raise_()
        self.sys_time_label_3.raise_()
        self.train_list_2.raise_()
        self.occupied_blocks.raise_()
        self.edit_schedule.raise_()
        self.add_stop.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.view_switcher.addWidget(self.train_view_page)

        #testbench
        self.testbench = QtWidgets.QWidget()
        self.testbench.setObjectName("testbench")
        self.red = QtWidgets.QRadioButton(self.testbench)
        self.red.setGeometry(QtCore.QRect(0, 570, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.red.setFont(font)
        self.red.setObjectName("red")
        self.train_label = QtWidgets.QComboBox(self.testbench)
        self.train_label.setGeometry(QtCore.QRect(0, 210, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.train_label.setFont(font)
        self.train_label.setObjectName("train_label")
        self.train_label.addItem("")
        self.system_speed_spnbx_4 = QtWidgets.QDoubleSpinBox(self.testbench)
        self.system_speed_spnbx_4.setGeometry(QtCore.QRect(910, 14, 62, 22))
        self.system_speed_spnbx_4.setObjectName("system_speed_spnbx_4")
        self.block_label = QtWidgets.QComboBox(self.testbench)
        self.block_label.setGeometry(QtCore.QRect(0, 50, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.block_label.setFont(font)
        self.block_label.setObjectName("block_label")
        self.block_label.addItem("")
        self.numPassengers = QtWidgets.QSpinBox(self.testbench)
        self.numPassengers.setGeometry(QtCore.QRect(180, 270, 51, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.numPassengers.setFont(font)
        self.numPassengers.setObjectName("numPassengers")
        self.light_label = QtWidgets.QComboBox(self.testbench)
        self.light_label.setGeometry(QtCore.QRect(0, 510, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.light_label.setFont(font)
        self.light_label.setObjectName("light_label")
        self.light_label.addItem("")
        self.curr_time_label = QtWidgets.QTextEdit(self.testbench)
        self.curr_time_label.setGeometry(QtCore.QRect(10, 140, 91, 31))
        self.curr_time_label.setObjectName("curr_time_label")
        self.num_passengers_label = QtWidgets.QTextEdit(self.testbench)
        self.num_passengers_label.setGeometry(QtCore.QRect(-1, 270, 171, 31))
        self.num_passengers_label.setObjectName("num_passengers_label")
        self.yellow = QtWidgets.QRadioButton(self.testbench)
        self.yellow.setGeometry(QtCore.QRect(0, 600, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.yellow.setFont(font)
        self.yellow.setObjectName("yellow")
        self.occupied_box = QtWidgets.QCheckBox(self.testbench)
        self.occupied_box.setGeometry(QtCore.QRect(10, 110, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.occupied_box.setFont(font)
        self.occupied_box.setObjectName("occupied_box")
        self.system_speed_label_4 = QtWidgets.QLabel(self.testbench)
        self.system_speed_label_4.setGeometry(QtCore.QRect(806, 10, 169, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.system_speed_label_4.setFont(font)
        self.system_speed_label_4.setAutoFillBackground(False)
        self.system_speed_label_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.system_speed_label_4.setObjectName("system_speed_label_4")
        self.left_right_label = QtWidgets.QTextEdit(self.testbench)
        self.left_right_label.setGeometry(QtCore.QRect(0, 430, 171, 51))
        self.left_right_label.setObjectName("left_right_label")
        self.back_button = QtWidgets.QPushButton(self.testbench)
        self.back_button.setGeometry(QtCore.QRect(620, 10, 81, 31))
        self.back_button.setObjectName("back_button")
        self.testbench_button.clicked.connect(self.open_main)
        self.green = QtWidgets.QRadioButton(self.testbench)
        self.green.setGeometry(QtCore.QRect(0, 630, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.green.setFont(font)
        self.green.setObjectName("green")
        self.curr_time_selector = QtWidgets.QTimeEdit(self.testbench)
        self.curr_time_selector.setGeometry(QtCore.QRect(10, 160, 91, 22))
        self.curr_time_selector.setObjectName("curr_time_selector")
        self.switchPos = QtWidgets.QSlider(self.testbench)
        self.switchPos.setGeometry(QtCore.QRect(40, 430, 81, 22))
        self.switchPos.setOrientation(QtCore.Qt.Horizontal)
        self.switchPos.setObjectName("switchPos")
        self.title_label_4 = QtWidgets.QLabel(self.testbench)
        self.title_label_4.setGeometry(QtCore.QRect(0, 0, 981, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title_label_4.setFont(font)
        self.title_label_4.setAutoFillBackground(False)
        self.title_label_4.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border: 3px solid black;")
        self.title_label_4.setObjectName("title_label_4")
        self.switch_label = QtWidgets.QComboBox(self.testbench)
        self.switch_label.setGeometry(QtCore.QRect(0, 370, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.switch_label.setFont(font)
        self.switch_label.setObjectName("switch_label")
        self.switch_label.addItem("")
        self.sys_time_label_4 = QtWidgets.QLabel(self.testbench)
        self.sys_time_label_4.setGeometry(QtCore.QRect(710, 10, 83, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sys_time_label_4.setFont(font)
        self.sys_time_label_4.setStyleSheet("border: 1px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.sys_time_label_4.setObjectName("sys_time_label_4")
        self.curr_vel_label = QtWidgets.QTextEdit(self.testbench)
        self.curr_vel_label.setGeometry(QtCore.QRect(0, 320, 91, 31))
        self.curr_vel_label.setObjectName("curr_vel_label")
        self.velocity_selector = QtWidgets.QSpinBox(self.testbench)
        self.velocity_selector.setGeometry(QtCore.QRect(90, 320, 61, 22))
        self.velocity_selector.setObjectName("velocity_selector")
        self.kmhr_label = QtWidgets.QTextEdit(self.testbench)
        self.kmhr_label.setGeometry(QtCore.QRect(150, 320, 41, 31))
        self.kmhr_label.setObjectName("kmhr_label")
        self.title_label_4.raise_()
        self.red.raise_()
        self.train_label.raise_()
        self.block_label.raise_()
        self.numPassengers.raise_()
        self.light_label.raise_()
        self.curr_time_label.raise_()
        self.num_passengers_label.raise_()
        self.yellow.raise_()
        self.occupied_box.raise_()
        self.system_speed_label_4.raise_()
        self.left_right_label.raise_()
        self.back_button.raise_()
        self.green.raise_()
        self.curr_time_selector.raise_()
        self.switchPos.raise_()
        self.switch_label.raise_()
        self.sys_time_label_4.raise_()
        self.curr_vel_label.raise_()
        self.velocity_selector.raise_()
        self.kmhr_label.raise_()
        self.system_speed_spnbx_4.raise_()
        self.view_switcher.addWidget(self.testbench)
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 980, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.view_switcher.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "self"))
        self.switch_auto.setText(_translate("self", "Switch to Automatic"))
        self.station_list.setItemText(0, _translate("self", "Destination Station"))
        self.confirm.setText(_translate("self", "Confirm"))
        self.system_speed_label_3.setText(_translate("self", " System Speed"))
        self.testbench_button.setText(_translate("self", "TESTBENCH"))
        self.header.setText(_translate("self", "Train View"))
        self.arrival_time_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Select Arrival Time</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.sys_time_label_3.setText(_translate("self", "13:24:55"))
        self.edit_schedule.setText(_translate("self", "Edit Schedule"))
        self.add_stop.setText(_translate("self", "Add Stop"))
        self.label.setText(_translate("self", "System Throughput: "))
        self.label_2.setText(_translate("self", "Schedule Train"))
        self.red.setText(_translate("self", "Red"))
        self.train_label.setItemText(0, _translate("self", "Train #"))
        self.block_label.setItemText(0, _translate("self", "Block X"))
        self.light_label.setItemText(0, _translate("self", "Light #"))
        self.curr_time_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Current Time</p></body></html>"))
        self.num_passengers_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Number of Passengers</span></p></body></html>"))
        self.yellow.setText(_translate("self", "Yellow"))
        self.occupied_box.setText(_translate("self", "Occupied"))
        self.system_speed_label_4.setText(_translate("self", " System Speed"))
        self.left_right_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Left            Right</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>"))
        self.back_button.setText(_translate("self", "BACK"))
        self.green.setText(_translate("self", "Green"))
        self.title_label_4.setText(_translate("self", "TESTBENCH"))
        self.switch_label.setItemText(0, _translate("self", "Switch X"))
        self.sys_time_label_4.setText(_translate("self", "13:24:55"))
        self.curr_vel_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Current Velocity</p></body></html>"))
        self.kmhr_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">km/hr</p></body></html>"))
            

    # update function
    def update(self):
        _translate = QtCore.QCoreApplication.translate

        # destination station and arrival time
        if self.ctc._trains[self.train_list.currentIndex()]._schedule != None:
            self.station_list.setCurrentText(self.ctc._trains[self.train_list.currentIndex()]._schedule.get_destination_station())
            self.station_list.setDisabled(True)

            arr_time = self.ctc._trains[self.train_list.currentIndex()]._schedule.get_arrival_time()
            real_arr_time = QTime(arr_time.hour, arr_time.minute)
            self.arrival_time.setTime(real_arr_time)
            self.arrival_time.setReadOnly(True)
            self.arrival_time.setButtonSymbols(QTimeEdit.NoButtons)
        else:
            self.station_list.setCurrentText("Destination Station")
            self.station_list.setDisabled(False)

            self.arrival_time.setTime(QTime.currentTime().addSecs(2 * 3600))
            self.arrival_time.setReadOnly(False)
            self.arrival_time.setButtonSymbols(QTimeEdit.UpDownArrows)

        # train schedule info
        temp_train = self.ctc._trains[self.train_list.currentIndex()]
        if temp_train._schedule != None:
            temp_dep_time_w_ms = temp_train.get_departure_time()
            temp_dep_time = time(temp_dep_time_w_ms.hour, temp_dep_time_w_ms.minute, temp_dep_time_w_ms.second)
            temp_auth = self.meters_to_miles(temp_train.get_authority())
            temp_sug_speed = self.kmhr_to_mihr(temp_train.get_suggested_velocity())
            temp_curr_speed = self.kmhr_to_mihr(temp_train.get_actual_velocity())


    # switch to testbench
    def open_testbench(self):
        self.view_switcher.setCurrentIndex(1)


    # switch to main screen
    def open_main(self):
        self.view_switcher.setCurrentIndex(0)


    # confirm button pressed, run checks then call ctc.py function
    def confirm_route(self, station_name, time_in, function, train_index):
        if datetime.now().time() < time_in and station_name != "Destination Station":
            self.ctc.create_schedule(station_name, time_in, function, train_index)
            self.update()
    

    # unit conversion functions
    def meters_to_miles(self, meters):
        return "{:.2f}".format(meters / 1609.344)
    def kmhr_to_mihr(self, kmhr):
        return "{:.2f}".format(kmhr / 0.621371)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    e = CTC_Main_UI(CTC(CTCTrackControllerAPI()))
    # self = QtWidgets.QMainWindow()
    # ui = CTC_Main_UI()
    # ui.setupUi(self)
    # self.show()
    sys.exit(app.exec_())
