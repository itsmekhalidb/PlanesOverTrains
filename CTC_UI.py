# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTC_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTime, QTimer
from datetime import datetime, time
from CTC import CTC

last_page = 0
CTC = CTC()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        global CTC

        # create blue line test
        CTC.test_blue_line_CTC()

        # create pages
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(981, 730)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.view_switcher = QtWidgets.QStackedWidget(self.centralwidget)
        self.view_switcher.setGeometry(QtCore.QRect(0, 0, 981, 730))
        self.view_switcher.setObjectName("view_switcher")

        # train view page
        self.train_view_page = QtWidgets.QWidget()
        self.train_view_page.setObjectName("train_view_page")
        self.switch_auto = QtWidgets.QPushButton(self.train_view_page)
        self.switch_auto.setGeometry(QtCore.QRect(810, 60, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.switch_auto.setFont(font)
        self.switch_auto.setObjectName("switch_auto")
        self.station_list = QtWidgets.QComboBox(self.train_view_page)
        self.station_list.setGeometry(QtCore.QRect(590, 210, 131, 22))
        self.station_list.setObjectName("station_list")
        self.station_list.addItem("Destination Station")
        for station_name in CTC.get_stations_names():
            self.station_list.addItem(station_name)
        self.system_speed_label_3 = QtWidgets.QLabel(self.train_view_page)
        self.system_speed_label_3.setGeometry(QtCore.QRect(806, 10, 169, 31))
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
        self.testbench_button.setGeometry(QtCore.QRect(620, 10, 81, 31))
        self.testbench_button.setObjectName("testbench_button")
        self.testbench_button.clicked.connect(self.show_testbench)
        self.arrival_time = QtWidgets.QTimeEdit(self.train_view_page)
        self.arrival_time.setGeometry(QtCore.QRect(620, 370, 81, 22))
        self.arrival_time.setObjectName("arrival_time")
        self.arrival_time.setTime(QTime.currentTime().addSecs(2 * 3600))
        self.dest_image = QtWidgets.QLabel(self.train_view_page)
        self.dest_image.setGeometry(QtCore.QRect(610, 240, 101, 101))
        self.dest_image.setObjectName("dest_image")
        self.track_image = QtWidgets.QLabel(self.train_view_page)
        self.track_image.setGeometry(QtCore.QRect(440, 260, 101, 71))
        self.track_image.setObjectName("track_image")
        self.train_info = QtWidgets.QTextEdit(self.train_view_page)
        self.train_info.setGeometry(QtCore.QRect(390, 400, 191, 91))
        self.train_info.setObjectName("train_info")
        self.train_info.setReadOnly(True)
        self.train_list = QtWidgets.QComboBox(self.train_view_page)
        self.train_list.setGeometry(QtCore.QRect(0, 50, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.train_list.setFont(font)
        self.train_list.setObjectName("train_list")
        for train in CTC.get_trains():
            self.train_list.addItem(train.train_list_info())
        self.train_image = QtWidgets.QLabel(self.train_view_page)
        self.train_image.setGeometry(QtCore.QRect(210, 190, 181, 181))
        self.train_image.setObjectName("train_image")
        self.system_speed_spnbx_3 = QtWidgets.QDoubleSpinBox(self.train_view_page)
        self.system_speed_spnbx_3.setGeometry(QtCore.QRect(910, 14, 62, 22))
        self.system_speed_spnbx_3.setObjectName("system_speed_spnbx_3")
        self.track_view = QtWidgets.QPushButton(self.train_view_page)
        self.track_view.setGeometry(QtCore.QRect(10, 640, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.track_view.setFont(font)
        self.track_view.setObjectName("track_view")
        self.track_view.clicked.connect(self.show_track_view)
        self.header = QtWidgets.QLabel(self.train_view_page)
        self.header.setGeometry(QtCore.QRect(0, 0, 981, 51))
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
        self.arrival_time_label.setGeometry(QtCore.QRect(610, 350, 101, 41))
        self.arrival_time_label.setObjectName("arrival_time_label")
        self.arrival_time_label.setReadOnly(True)
        self.sys_time_label_3 = QtWidgets.QLabel(self.train_view_page)
        self.sys_time_label_3.setGeometry(QtCore.QRect(710, 10, 83, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sys_time_label_3.setFont(font)
        self.sys_time_label_3.setStyleSheet("border: 1px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.sys_time_label_3.setObjectName("sys_time_label_3")
        self.confirm = QtWidgets.QPushButton(self.train_view_page)
        self.confirm.setGeometry(QtCore.QRect(450, 520, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm.setFont(font)
        self.confirm.setObjectName("confirm")
        not_qtime = time(self.arrival_time.time().hour(), self.arrival_time.time().minute(), self.arrival_time.time().second())
        self.confirm.clicked.connect(lambda:self.confirm_route(self.station_list.currentText(), not_qtime, self.train_list.currentIndex()))
        self.arrival_time_label.raise_()
        self.header.raise_()
        self.switch_auto.raise_()
        self.station_list.raise_()
        self.confirm.raise_()
        self.system_speed_label_3.raise_()
        self.testbench_button.raise_()
        self.arrival_time.raise_()
        self.dest_image.raise_()
        self.track_image.raise_()
        self.train_info.raise_()
        self.train_list.raise_()
        self.train_image.raise_()
        self.system_speed_spnbx_3.raise_()
        self.track_view.raise_()
        self.sys_time_label_3.raise_()
        self.view_switcher.addWidget(self.train_view_page)

        # track view page
        self.track_view_page = QtWidgets.QWidget()
        self.track_view_page.setObjectName("track_view_page")
        self.key_header = QtWidgets.QTextEdit(self.track_view_page)
        self.key_header.setGeometry(QtCore.QRect(10, 60, 71, 51))
        self.key_header.setObjectName("key_header")
        self.key_header.setReadOnly(True)
        self.station_icon = QtWidgets.QLabel(self.track_view_page)
        self.station_icon.setGeometry(QtCore.QRect(10, 110, 31, 31))
        self.station_icon.setObjectName("station_icon")
        self.track_map = QtWidgets.QGraphicsView(self.track_view_page)
        self.track_map.setGeometry(QtCore.QRect(170, 61, 481, 621))
        self.track_map.setObjectName("track_map")
        self.closure_icon = QtWidgets.QLabel(self.track_view_page)
        self.closure_icon.setGeometry(QtCore.QRect(10, 200, 31, 31))
        self.closure_icon.setObjectName("closure_icon")
        self.element_info = QtWidgets.QTextEdit(self.track_view_page)
        self.element_info.setGeometry(QtCore.QRect(670, 150, 301, 241))
        self.element_info.setObjectName("element_info")
        self.element_info.setReadOnly(True)
        self.occupiedBlocks = QtWidgets.QScrollArea(self.track_view_page)
        self.occupiedBlocks.setGeometry(QtCore.QRect(669, 419, 301, 261))
        self.occupiedBlocks.setWidgetResizable(True)
        self.occupiedBlocks.setObjectName("occupiedBlocks")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 299, 259))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.occupiedBlocks.setWidget(self.scrollAreaWidgetContents)
        self.system_speed_spnbx_2 = QtWidgets.QDoubleSpinBox(self.track_view_page)
        self.system_speed_spnbx_2.setGeometry(QtCore.QRect(910, 14, 62, 22))
        self.system_speed_spnbx_2.setObjectName("system_speed_spnbx_2")
        self.title_label_2 = QtWidgets.QLabel(self.track_view_page)
        self.title_label_2.setGeometry(QtCore.QRect(0, 0, 981, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title_label_2.setFont(font)
        self.title_label_2.setAutoFillBackground(False)
        self.title_label_2.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border: 3px solid black;")
        self.title_label_2.setObjectName("title_label_2")
        self.element_header = QtWidgets.QTextEdit(self.track_view_page)
        self.element_header.setGeometry(QtCore.QRect(670, 60, 301, 91))
        self.element_header.setObjectName("element_header")
        self.element_header.setReadOnly(True)
        self.sys_time_label_2 = QtWidgets.QLabel(self.track_view_page)
        self.sys_time_label_2.setGeometry(QtCore.QRect(710, 10, 83, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sys_time_label_2.setFont(font)
        self.sys_time_label_2.setStyleSheet("border: 1px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.sys_time_label_2.setObjectName("sys_time_label_2")
        self.train_view = QtWidgets.QPushButton(self.track_view_page)
        self.train_view.setGeometry(QtCore.QRect(20, 630, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.train_view.setFont(font)
        self.train_view.setObjectName("train_view")
        self.train_view.clicked.connect(self.show_train_view)
        self.key_labels = QtWidgets.QTextEdit(self.track_view_page)
        self.key_labels.setGeometry(QtCore.QRect(40, 110, 111, 131))
        self.key_labels.setObjectName("key_labels")
        self.key_labels.setReadOnly(True)
        self.track_icon = QtWidgets.QLabel(self.track_view_page)
        self.track_icon.setGeometry(QtCore.QRect(10, 170, 31, 31))
        self.track_icon.setObjectName("track_icon")
        self.system_speed_label_2 = QtWidgets.QLabel(self.track_view_page)
        self.system_speed_label_2.setGeometry(QtCore.QRect(806, 10, 169, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.system_speed_label_2.setFont(font)
        self.system_speed_label_2.setAutoFillBackground(False)
        self.system_speed_label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.system_speed_label_2.setObjectName("system_speed_label_2")
        self.testbench_2 = QtWidgets.QPushButton(self.track_view_page)
        self.testbench_2.setGeometry(QtCore.QRect(620, 10, 81, 31))
        self.testbench_2.setObjectName("testbench_2")
        self.testbench_2.clicked.connect(self.show_testbench)
        self.import_map = QtWidgets.QPushButton(self.track_view_page)
        self.import_map.setGeometry(QtCore.QRect(40, 580, 91, 23))
        self.import_map.setObjectName("import_map")
        self.train_icon = QtWidgets.QLabel(self.track_view_page)
        self.train_icon.setGeometry(QtCore.QRect(10, 140, 31, 31))
        self.train_icon.setObjectName("train_icon")
        self.key_header.raise_()
        self.station_icon.raise_()
        self.track_map.raise_()
        self.closure_icon.raise_()
        self.element_info.raise_()
        self.occupiedBlocks.raise_()
        self.title_label_2.raise_()
        self.element_header.raise_()
        self.sys_time_label_2.raise_()
        self.train_view.raise_()
        self.key_labels.raise_()
        self.track_icon.raise_()
        self.system_speed_label_2.raise_()
        self.testbench_2.raise_()
        self.import_map.raise_()
        self.train_icon.raise_()
        self.system_speed_spnbx_2.raise_()
        self.view_switcher.addWidget(self.track_view_page)

        # testbench view
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
        self.curr_time_label.setReadOnly(True)
        self.num_passengers_label = QtWidgets.QTextEdit(self.testbench)
        self.num_passengers_label.setGeometry(QtCore.QRect(-1, 270, 171, 31))
        self.num_passengers_label.setObjectName("num_passengers_label")
        self.num_passengers_label.setReadOnly(True)
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
        self.left_right_label.setReadOnly(True)
        self.back_button = QtWidgets.QPushButton(self.testbench)
        self.back_button.setGeometry(QtCore.QRect(620, 10, 81, 31))
        self.back_button.setObjectName("back_button")
        self.back_button.clicked.connect(self.leave_testbench)
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
        self.curr_vel_label.setReadOnly(True)
        self.velocity_selector = QtWidgets.QSpinBox(self.testbench)
        self.velocity_selector.setGeometry(QtCore.QRect(90, 320, 61, 22))
        self.velocity_selector.setObjectName("velocity_selector")
        self.kmhr_label = QtWidgets.QTextEdit(self.testbench)
        self.kmhr_label.setGeometry(QtCore.QRect(150, 320, 41, 31))
        self.kmhr_label.setObjectName("kmhr_label")
        self.kmhr_label.setReadOnly(True)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 981, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.view_switcher.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # set default page 
        self.view_switcher.setCurrentIndex(1)

    

    def retranslateUi(self, MainWindow):
        global CTC
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.switch_auto.setText(_translate("MainWindow", "Switch to Automatic"))
        self.confirm.setText(_translate("MainWindow", "Confirm"))
        self.system_speed_label_3.setText(_translate("MainWindow", " System Speed"))
        self.testbench_button.setText(_translate("MainWindow", "TESTBENCH"))
        self.dest_image.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/train_image/CTC_resources/station.png\"/></p></body></html>"))
        self.track_image.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/train_image/CTC_resources/track.png\"/></p></body></html>"))
        self.train_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Departure Time: </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Authority: </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Suggested Speed: </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Speed: </span></p></body></html>"))
        self.train_image.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/train_image/CTC_resources/train.png\"/></p></body></html>"))
        self.track_view.setText(_translate("MainWindow", "Track View"))
        self.header.setText(_translate("MainWindow", "Train View"))
        self.arrival_time_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Select Arrival Time</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.sys_time_label_3.setText(_translate("MainWindow", "13:24:55"))
        self.key_header.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Key</span></p></body></html>"))
        self.station_icon.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/KeyIcons/CTC_resources/station_small.png\"/></p></body></html>"))
        self.closure_icon.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/KeyIcons/CTC_resources/closed_small.png\"/></p></body></html>"))
        self.element_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">info info blah blah</span></p></body></html>"))
        self.title_label_2.setText(_translate("MainWindow", "Track View"))
        self.element_header.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:24pt;\">Select an element to view info</span></p></body></html>"))
        self.sys_time_label_2.setText(_translate("MainWindow", "13:24:55"))
        self.train_view.setText(_translate("MainWindow", "Train View"))
        self.key_labels.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Stations</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Trains</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Track</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt;\">Closure</span></p></body></html>"))
        self.track_icon.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/KeyIcons/CTC_resources/track_line.png\"/></p></body></html>"))
        self.system_speed_label_2.setText(_translate("MainWindow", " System Speed"))
        self.testbench_2.setText(_translate("MainWindow", "TESTBENCH"))
        self.import_map.setText(_translate("MainWindow", "Import Map"))
        self.train_icon.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/KeyIcons/CTC_resources/train_small.png\"/></p></body></html>"))
        self.red.setText(_translate("MainWindow", "Red"))
        self.train_label.setItemText(0, _translate("MainWindow", "Train #"))
        self.block_label.setItemText(0, _translate("MainWindow", "Block X"))
        self.light_label.setItemText(0, _translate("MainWindow", "Light #"))
        self.curr_time_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Current Time</p></body></html>"))
        self.num_passengers_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Number of Passengers</span></p></body></html>"))
        self.yellow.setText(_translate("MainWindow", "Yellow"))
        self.occupied_box.setText(_translate("MainWindow", "Occupied"))
        self.system_speed_label_4.setText(_translate("MainWindow", " System Speed"))
        self.left_right_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Left                   Right</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:12pt;\"><br /></p></body></html>"))
        self.back_button.setText(_translate("MainWindow", "BACK"))
        self.green.setText(_translate("MainWindow", "Green"))
        self.title_label_4.setText(_translate("MainWindow", "TESTBENCH"))
        self.switch_label.setItemText(0, _translate("MainWindow", "Switch X"))
        self.sys_time_label_4.setText(_translate("MainWindow", "13:24:55"))
        self.curr_vel_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Current Velocity</p></body></html>"))
        self.kmhr_label.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">km/hr</p></body></html>"))
    

    # update function
    def update(self):
        global CTC
        _translate = QtCore.QCoreApplication.translate

        # train schedule info
        temp_train = CTC._trains[self.train_list.currentIndex()]
        if temp_train._schedule != None:
            temp_dep_time_w_ms = temp_train.get_departure_time()
            temp_dep_time = time(temp_dep_time_w_ms.hour, temp_dep_time_w_ms.minute, temp_dep_time_w_ms.second)
            temp_auth = temp_train.get_authority()
            temp_sug_speed = temp_train.get_suggested_velocity()
            temp_curr_speed = temp_train.get_actual_velocity()
            self.train_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Departure Time: {temp_dep_time}</span></p>\n"
        f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Authority: {temp_auth}</span></p>\n"
        f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Suggested Speed: {temp_sug_speed}</span></p>\n"
        f"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Speed: {temp_curr_speed}</span></p></body></html>"))
        else:
            self.train_info.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Departure Time: </span></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Authority: </span></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Suggested Speed: </span></p>\n"
        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Speed: </span></p></body></html>"))


    # switch to train view
    def show_train_view(self):
        self.view_switcher.setCurrentIndex(0)


    # switch to track view
    def show_track_view(self):
        self.view_switcher.setCurrentIndex(1)


    # switch to testbench
    def show_testbench(self):
        global last_page
        last_page = self.view_switcher.currentIndex()
        self.view_switcher.setCurrentIndex(2)


    # leave testbench
    def leave_testbench(self):
        global last_page
        self.view_switcher.setCurrentIndex(last_page)


    # confirm button pressed, run checks then call ctc.py function
    def confirm_route(self, station_name, time_in, train_index):
        global CTC
        if datetime.now().time() < time_in and station_name != "Destination Station":
            CTC._trains[train_index].create_schedule(station_name, time_in, CTC._track)
            self.update()


    def test(self):
        print("help")
        

import CTC_resource_file_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
