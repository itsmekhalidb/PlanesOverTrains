# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CTC_Train_UI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(981, 730)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title_label_3 = QtWidgets.QLabel(self.centralwidget)
        self.title_label_3.setGeometry(QtCore.QRect(0, 0, 981, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.title_label_3.setFont(font)
        self.title_label_3.setAutoFillBackground(False)
        self.title_label_3.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"border: 3px solid black;")
        self.title_label_3.setObjectName("title_label_3")
        self.system_speed_label_3 = QtWidgets.QLabel(self.centralwidget)
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
        self.system_speed_spnbx_3 = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.system_speed_spnbx_3.setGeometry(QtCore.QRect(910, 14, 62, 22))
        self.system_speed_spnbx_3.setObjectName("system_speed_spnbx_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(620, 10, 81, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.sys_time_label_3 = QtWidgets.QLabel(self.centralwidget)
        self.sys_time_label_3.setGeometry(QtCore.QRect(710, 10, 83, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.sys_time_label_3.setFont(font)
        self.sys_time_label_3.setStyleSheet("border: 1px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.sys_time_label_3.setObjectName("sys_time_label_3")
        self.arrivalTime = QtWidgets.QTimeEdit(self.centralwidget)
        self.arrivalTime.setGeometry(QtCore.QRect(620, 370, 81, 22))
        self.arrivalTime.setObjectName("arrivalTime")
        self.textEdit_5 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_5.setGeometry(QtCore.QRect(610, 350, 101, 41))
        self.textEdit_5.setObjectName("textEdit_5")
        self.toolButton_2 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_2.setGeometry(QtCore.QRect(600, 210, 121, 19))
        self.toolButton_2.setObjectName("toolButton_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(450, 520, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(390, 400, 191, 91))
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(810, 60, 161, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 190, 181, 181))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 260, 101, 71))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(610, 240, 101, 101))
        self.label_3.setObjectName("label_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 640, 131, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(0, 50, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.raise_()
        self.textEdit.raise_()
        self.textEdit_5.raise_()
        self.title_label_3.raise_()
        self.system_speed_label_3.raise_()
        self.system_speed_spnbx_3.raise_()
        self.pushButton_3.raise_()
        self.sys_time_label_3.raise_()
        self.arrivalTime.raise_()
        self.toolButton_2.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.pushButton_4.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 981, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.title_label_3.setText(_translate("MainWindow", "Train View"))
        self.system_speed_label_3.setText(_translate("MainWindow", " System Speed"))
        self.pushButton_3.setText(_translate("MainWindow", "TESTBENCH"))
        self.sys_time_label_3.setText(_translate("MainWindow", "13:24:55"))
        self.textEdit_5.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Select Arrival Time</span></p>\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p></body></html>"))
        self.toolButton_2.setText(_translate("MainWindow", "Destination Station"))
        self.pushButton.setText(_translate("MainWindow", "Confirm"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Departure Time: </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Authority: </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Suggested Speed: </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Current Speed: </span></p></body></html>"))
        self.pushButton_2.setText(_translate("MainWindow", "Switch to Automatic"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/train_image/CTC_resources/train.png\"/></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/train_image/CTC_resources/track.png\"/></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/train_image/CTC_resources/station.png\"/></p></body></html>"))
        self.pushButton_4.setText(_translate("MainWindow", "Map View"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Train # - Outbound"))
import CTC_resource_file


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
