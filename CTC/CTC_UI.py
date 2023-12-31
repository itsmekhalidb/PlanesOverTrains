# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTC_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import typing
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTimeEdit, QApplication, QTableView, QHeaderView, QMainWindow, QWidget, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime, time
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from CTC import CTC

from api.ctc_track_controller_api import CTCTrackControllerAPI
from api.ctc_track_model_api import CTCTrackModelAPI

last_page = 0
train_nums = []


class CTC_Main_UI(QMainWindow):

    def __init__(self, ctc : CTC) -> None:
        super().__init__()
        self.ctc = ctc
        self.lock = 0 # lock ui elements from updating after fp loaded in
        self.setupUi()
        self.show()

    def setupUi(self):

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
        self.switch_auto.clicked.connect(lambda:self.open_file())
        self.arrival_time = QtWidgets.QTimeEdit(self.train_view_page)
        self.arrival_time.setGeometry(QtCore.QRect(15, 430, 81, 22))
        self.arrival_time.setObjectName("arrival_time")
        self.arrival_time.setDisplayFormat("HH:mm:ss")
        self.arrival_time.setTime(self.datetime_to_qtime(self.ctc.get_time()).addSecs(2 * 60))
        self.station_list = QtWidgets.QComboBox(self.train_view_page)
        self.station_list.setGeometry(QtCore.QRect(5, 370, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.station_list.setFont(font)
        self.station_list.setObjectName("station_list")
        self.station_list.addItem("Destination Station")
        self.confirm = QtWidgets.QPushButton(self.train_view_page)
        self.confirm.setGeometry(QtCore.QRect(5, 460, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm.setFont(font)
        self.confirm.setObjectName("confirm")
        # self._not_qtime = self.qtime_to_datetime(self.arrival_time.time())
        # self.arrival_time.timeChanged.connect(lambda:self.update_not_qtime())
        mode = 0 # mode 0 is new train, 1 is adding a stop, 2 is editing the schedule
        train_index = -1 # -1 if creating new train, otherwise use train index
        self.confirm.clicked.connect(lambda:self.confirm_route(self.station_list.currentText(), self.qtime_to_datetime(self.arrival_time.time()), mode, train_index))
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
        # self.testbench_button = QtWidgets.QPushButton(self.train_view_page)
        # self.testbench_button.setGeometry(QtCore.QRect(315, 10, 81, 31))
        # self.testbench_button.setObjectName("testbench_button")
        # self.testbench_button.clicked.connect(self.open_testbench)
        self.system_speed_spnbx_3 = QtWidgets.QDoubleSpinBox(self.train_view_page)
        self.system_speed_spnbx_3.setGeometry(QtCore.QRect(605, 14, 62, 22))
        self.system_speed_spnbx_3.setObjectName("system_speed_spnbx_3")
        self.system_speed_spnbx_3.setMaximum(10)
        self.system_speed_spnbx_3.setMinimum(0)
        self.system_speed_spnbx_3.setValue(1)
        self.system_speed_spnbx_3.setValue(self.ctc.get_time_scaling())
        self.system_speed_spnbx_3.valueChanged.connect(lambda:self.change_time_speed(self.system_speed_spnbx_3.value(), 0))
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
        self.arrival_time_label.setGeometry(QtCore.QRect(5, 410, 101, 41))
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
        self.train_list_2.verticalHeader().setVisible(False)

        # data = [ # code to add data
        #     ["1", "08:00", "10:30", "East Liberty", "890 m", "89 mi/hr", "50 mi/hr"]
        #     # Add more rows as needed
        # ]

        # for row_index, row_data in enumerate(data):
        #     for column_index, cell_data in enumerate(row_data):
        #         item = QStandardItem(str(cell_data))
        #         self.train_list_2_data.setItem(row_index, column_index, item)

        self.occupied_blocks = QtWidgets.QScrollArea(self.train_view_page)
        self.occupied_blocks.setGeometry(QtCore.QRect(514, 320, 161, 281))
        self.occupied_blocks.setWidgetResizable(True)
        self.occupied_blocks.setObjectName("occupied_blocks")
        self.blocks_table_widget = QtWidgets.QWidget()
        self.blocks_table_widget.setGeometry(QtCore.QRect(0, 0, 159, 139))
        self.blocks_table_widget.setObjectName("blocks_table_widget")
        self.blocks_table = QtWidgets.QTableWidget(self.blocks_table_widget)
        self.blocks_table.setGeometry(QtCore.QRect(0, 0, 161, 281))
        self.blocks_table.setObjectName("blocks_table")
        self.blocks_table.setColumnCount(1)
        self.blocks_table.setRowCount(0)
        self.blocks_table.setHorizontalHeaderItem(0, QTableWidgetItem("Occupied Blocks"))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.blocks_table.horizontalHeaderItem(0).setFont(font)
        self.blocks_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.occupied_blocks.setWidget(self.blocks_table_widget)
        self.edit_schedule = QtWidgets.QPushButton(self.train_view_page)
        self.edit_schedule.setGeometry(QtCore.QRect(5, 400, 121, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.edit_schedule.setFont(font)
        self.edit_schedule.setObjectName("edit_schedule")
        self.edit_schedule.hide()
        self.add_stop = QtWidgets.QPushButton(self.train_view_page)
        self.add_stop.setGeometry(QtCore.QRect(5, 360, 101, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_stop.setFont(font)
        self.add_stop.setObjectName("add_stop")
        self.add_stop.hide()
        self.label = QtWidgets.QLabel(self.train_view_page)
        self.label.setGeometry(QtCore.QRect(182, 611, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.train_view_page)
        self.label_2.setGeometry(QtCore.QRect(5, 330, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.block_close_label = QtWidgets.QLabel(self.train_view_page)
        self.block_close_label.setGeometry(QtCore.QRect(290, 330, 231, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.block_close_label.setFont(font)
        self.block_close_label.setObjectName("block_close_label")
        self.section_list = QtWidgets.QComboBox(self.train_view_page)
        self.section_list.setGeometry(QtCore.QRect(410, 370, 95, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.section_list.setFont(font)
        self.section_list.setObjectName("section_list")
        self.section_list.addItem("Section")
        self.block_list = QtWidgets.QComboBox(self.train_view_page)
        self.block_list.setGeometry(QtCore.QRect(425, 410, 80, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.block_list.setFont(font)
        self.block_list.setObjectName("block_list")
        self.block_list.addItem("Block")
        self.section_list.currentIndexChanged.connect(lambda:self.block_list.addItems(self.initialize_block_list("green", self.section_list.currentText(), self.block_list)))
        self.confirm_close = QtWidgets.QPushButton(self.train_view_page)
        self.confirm_close.setGeometry(QtCore.QRect(425, 450, 81, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm_close.setFont(font)
        self.confirm_close.setObjectName("confirm_close")
        self.confirm_close.clicked.connect(lambda:self.change_block(self.section_list.currentText(), self.block_list.currentText()))
        not_qtime = time(self.arrival_time.time().hour(), self.arrival_time.time().minute(), self.arrival_time.time().second())
        self.arrival_time_label.raise_()
        self.header.raise_()
        self.switch_auto.raise_()
        self.station_list.raise_()
        self.confirm.raise_()
        self.system_speed_label_3.raise_()
        # self.testbench_button.raise_()
        self.arrival_time.raise_()
        self.system_speed_spnbx_3.raise_()
        self.sys_time_label_3.raise_()
        self.train_list_2.raise_()
        self.occupied_blocks.raise_()
        self.edit_schedule.raise_()
        self.add_stop.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.block_close_label.raise_()
        self.section_list.raise_()
        self.confirm_close.raise_()
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
        self.system_speed_spnbx_4.setGeometry(QtCore.QRect(605, 14, 62, 22))
        self.system_speed_spnbx_4.setObjectName("system_speed_spnbx_4")
        self.system_speed_spnbx_4.setMaximum(10)
        self.system_speed_spnbx_4.setMinimum(1)
        self.system_speed_spnbx_4.valueChanged.connect(lambda:self.change_time_speed(self.system_speed_spnbx_4.value(), 1))
        self.block_label = QtWidgets.QComboBox(self.testbench)
        self.block_label.setGeometry(QtCore.QRect(181, 53, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.block_label.setFont(font)
        self.block_label.setObjectName("block_label")
        self.block_label.addItem("")
        self.section_label = QtWidgets.QComboBox(self.testbench)
        self.section_label.setGeometry(QtCore.QRect(0, 53, 171, 51))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.section_label.setFont(font)
        self.section_label.setObjectName("section_label")
        self.section_label.addItem("")
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
        self.num_passengers_label = QtWidgets.QTextEdit(self.testbench)
        self.num_passengers_label.setGeometry(QtCore.QRect(-1, 270, 171, 31))
        self.num_passengers_label.setObjectName("num_passengers_label")
        self.occupied_box = QtWidgets.QCheckBox(self.testbench)
        self.occupied_box.setGeometry(QtCore.QRect(10, 110, 91, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.occupied_box.setFont(font)
        self.occupied_box.setObjectName("occupied_box")
        self.system_speed_label_4 = QtWidgets.QLabel(self.testbench)
        self.system_speed_label_4.setGeometry(QtCore.QRect(501, 10, 169, 31))
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
        self.back_button.setGeometry(QtCore.QRect(315, 10, 81, 31))
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(lambda:self.open_main())
        self.green = QtWidgets.QRadioButton(self.testbench)
        self.green.setGeometry(QtCore.QRect(0, 600, 82, 17))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.green.setFont(font)
        self.green.setObjectName("green")
        self.switchPos = QtWidgets.QSlider(self.testbench)
        self.switchPos.setGeometry(QtCore.QRect(40, 430, 81, 22))
        self.switchPos.setOrientation(QtCore.Qt.Horizontal)
        self.switchPos.setObjectName("switchPos")
        self.title_label_4 = QtWidgets.QLabel(self.testbench)
        self.title_label_4.setGeometry(QtCore.QRect(0, 0, 676, 51))
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
        self.sys_time_label_4.setGeometry(QtCore.QRect(405, 10, 83, 31))
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
        self.section_label.raise_()
        self.numPassengers.raise_()
        self.light_label.raise_()
        self.num_passengers_label.raise_()
        self.occupied_box.raise_()
        self.system_speed_label_4.raise_()
        self.left_right_label.raise_()
        self.back_button.raise_()
        self.green.raise_()
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

        self._handler()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "CTC"))
        self.switch_auto.setText(_translate("self", "Switch to Automatic"))
        self.station_list.setItemText(0, _translate("self", "Destination Station"))
        self.confirm.setText(_translate("self", "Confirm"))
        self.confirm_close.setText(_translate("self", "Confirm"))
        self.system_speed_label_3.setText(_translate("self", " System Speed"))
        # self.testbench_button.setText(_translate("self", "Testbench"))
        self.header.setText(_translate("self", "green Line"))
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
        self.block_close_label.setText(_translate("self", "Maintenance Mode"))
        self.red.setText(_translate("self", "Red"))
        self.train_label.setItemText(0, _translate("self", "Train #"))
        self.block_label.setItemText(0, _translate("self", "Block #"))
        self.section_label.setItemText(0, _translate("self", "Section"))
        self.light_label.setItemText(0, _translate("self", "Light #"))
        self.num_passengers_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Number of Passengers</span></p></body></html>"))
        self.occupied_box.setText(_translate("self", "Occupied"))
        self.system_speed_label_4.setText(_translate("self", " System Speed"))
        self.left_right_label.setHtml(_translate("self", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Left                   Right</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>"))
        self.back_button.setText(_translate("self", "BACK"))
        self.green.setText(_translate("self", "green"))
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
            
    
    def update(self, thread=False):
        global train_nums
        temp_time = self.ctc.get_time()
        hr = str(temp_time.hour)
        min = str(temp_time.minute)
        sec = str(temp_time.second)
        if len(hr) == 1:
            hr = "0" + hr
        if len(min) == 1:
            min = "0" + min
        if len(sec) == 1:
            sec = "0" + sec
        temp_timestr = hr + ":" + min + ":" + sec
        self.sys_time_label_3.setText(temp_timestr)
        self.sys_time_label_4.setText(temp_timestr)

        if (self.ctc.check_filepath()):
            if (self.lock == 0 and self.ctc.TrackCTRLSignal._track_info != {}):
                self.section_list.addItems(self.initialize_section_list("green"))
                self.station_list.addItems(list(self.ctc.get_stations()['green']))
                self.lock = 1

            # update train info
            for train in self.ctc.get_trains():
                train_num = train.get_train_number()
                if train_num not in train_nums:
                    train_nums.append(train_num)
                    row = [
                        QStandardItem(str(train_num)),
                        QStandardItem(self.leading_zero(train.get_departure_time().hour) + ":" + self.leading_zero(train.get_departure_time().minute)),
                        QStandardItem(self.leading_zero(train.get_arrival_time().hour) + ":" + self.leading_zero(train.get_arrival_time().minute)),
                        QStandardItem(train.get_dest_station()),
                        QStandardItem(str(self.meters_to_miles(train.get_total_authority())) + " mi"),
                        QStandardItem(str(self.kmhr_to_mihr(70)) + " mi/hr"), # CHANGE CHANGE CHANGE CHANGE
                        QStandardItem(str(self.ctc.update_curr_speed(train_num)) + " mi/hr")
                    ]
                    # print(row)
                    self.train_list_2_data.appendRow(row)
                else:
                    if self.train_list_2_data.item(train_nums.index(train_num), 3) != None:
                        #print(self.meters_to_miles(train.get_total_authority()))
                        self.train_list_2_data.item(train_nums.index(train_num), 3).setData(str(self.meters_to_miles(train.get_total_authority())) + " mi")
                        #self.train_list_2_data.item(train_nums.index(train_num), 4).setData(str(self.kmhr_to_mihr(train.get_suggested_velocity())) + " mi/hr")
                        self.train_list_2_data.item(train_nums.index(train_num), 4).setData(str(self.kmhr_to_mihr(70)) + " mi/hr")
                        self.train_list_2_data.item(train_nums.index(train_num), 5).setData(str(self.ctc.update_curr_speed(train_num)) + " mi/hr")
            
            # update occupied blocks
            cntr = 0
            for block in self.ctc.get_occupancy():
                self.blocks_table.setItem(cntr, 0, QTableWidgetItem(block))
            
            # update throughput
            tp = "Throughput " + str(self.ctc.get_throughput()) + " people/hr"
            self.label.setText(tp)


    def _handler(self):
            self.timer = QTimer()
            self.timer.setInterval(100)  # refreshes every time period
            self.timer.timeout.connect(self.update)
            self.timer.start()


    # switch to testbench
    def open_testbench(self):
        self.view_switcher.setCurrentIndex(1)


    # switch to main screen
    def open_main(self):
        self.view_switcher.setCurrentIndex(0)
    

    # open scheduling file
    def open_file(self):
        # create a Tkinter root window (it will not be shown)
        root = tk.Tk()
        root.withdraw()  # hide the main window
        
        # ask the user to select an Excel file
        file_path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx;*.xls")],
        )
        
        # check if the user selected a file
        if file_path:
            try:
                doc = pd.read_excel(file_path)
                print("Successfully imported Excel file")
                self.ctc.import_schedule(doc)
            except Exception as e:
                print(f"Error reading Excel file: {e}")
        else:
            print("No file selected.")


    # confirm button pressed, run checks then call ctc.py function
    def confirm_route(self, station_name, time_in, function, train_index):
        if self.ctc.get_time() < time_in and station_name != "Destination Station" and self.ctc.check_filepath():
            self.ctc.create_schedule(station_name, time_in, function, train_index)
        elif not self.ctc.check_filepath():
            print("Track Model data not initialized")
    

    # change time speed when spinbox changed
    def change_time_speed(self, speed, screen):
        self.ctc.set_time_scaling(speed)
        if screen == 0:
            self.system_speed_spnbx_4.setValue(speed)
        else:
            self.system_speed_spnbx_3.setValue(speed)
    

    # display section names
    def initialize_section_list(self, line):
        return sorted(self.ctc.get_sections(line))
    

    # display block numbers
    def initialize_block_list(self, line, section_name, block_list):
        block_list.clear()
        block_list.addItem("Block")
        return self.ctc.get_blocks(line, section_name)
    
    
    # close block
    def change_block(self, section, block):
        name = section + block
        self.ctc.change_block(name)

    # update notqtime
    def update_not_qtime(self):
        self._not_qtime = self.qtime_to_datetime(self.arrival_time.time())

    # unit conversion functions
    def meters_to_miles(self, meters):
        return "{:.2f}".format(meters / 1609.344)
    def kmhr_to_mihr(self, kmhr):
        return "{:.2f}".format(kmhr / 0.621371)
    def datetime_to_qtime(self, dt):
        return QTime(dt.hour, dt.minute, dt.second)
    def qtime_to_datetime(self, qt):
        current_date = datetime.now().date()
        return datetime(current_date.year, current_date.month, current_date.day, qt.hour(), qt.minute(), qt.second())
    # add leading zero
    def leading_zero(self, num):
        if len(str(num)) == 1:
            return str(0) + str(num)
        else:
            return str(num)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    e = CTC_Main_UI(CTC(CTCTrackControllerAPI()))
    # self = QtWidgets.QMainWindow()
    # ui = CTC_Main_UI()
    # ui.setupUi(self)
    # self.show()
    sys.exit(app.exec_())
