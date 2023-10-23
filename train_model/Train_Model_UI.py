from PyQt5 import QtCore, QtGui, QtWidgets
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
from train_model.train_model import TrainModel
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from api.train_model_train_controller_api import TrainModelTrainControllerAPI

class Ui_TrainModel_MainUI(QMainWindow):

        def __init__(self, train_model: TrainModel) -> None:
                super().__init__()
                self.train_model = train_model
                self.setupUi()
                self.show()

        def setupUi(self):
                self.setObjectName("self")
                self.resize(679, 569)
                self.setStyleSheet("background-color: rgb(255, 255, 255);")
                self.centralwidget = QtWidgets.QWidget(self)
                self.centralwidget.setObjectName("centralwidget")
                self.title_label = QtWidgets.QLabel(self.centralwidget)
                self.title_label.setGeometry(QtCore.QRect(0, 0, 679, 51))
                font = QtGui.QFont()
                font.setPointSize(16)
                font.setBold(True)
                font.setWeight(75)
                self.title_label.setFont(font)
                self.title_label.setAutoFillBackground(False)
                self.title_label.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                "border: 3px solid black;")
                self.title_label.setObjectName("title_label")
                # self.system_speed_spnbx = QtWidgets.QDoubleSpinBox(self.centralwidget)
                # self.system_speed_spnbx.setGeometry(QtCore.QRect(604, 12, 62, 22))
                # self.system_speed_spnbx.setObjectName("system_speed_spnbx")
                # self.system_speed_label = QtWidgets.QLabel(self.centralwidget)
                # self.system_speed_label.setGeometry(QtCore.QRect(500, 8, 169, 31))
                # font = QtGui.QFont()
                # font.setPointSize(10)
                # font.setBold(True)
                # font.setWeight(75)
                # self.system_speed_label.setFont(font)
                # self.system_speed_label.setAutoFillBackground(False)
                # self.system_speed_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                # "border: 1px solid black;")
                # self.system_speed_label.setObjectName("system_speed_label")
                # self.sys_time_label = QtWidgets.QLabel(self.centralwidget)
                # self.sys_time_label.setGeometry(QtCore.QRect(406, 8, 83, 31))
                # font = QtGui.QFont()
                # font.setPointSize(12)
                # font.setBold(True)
                # font.setWeight(75)
                # self.sys_time_label.setFont(font)
                # self.sys_time_label.setStyleSheet("border: 1px solid black;\n"
                # "background-color: rgb(255, 255, 255);")
                # self.sys_time_label.setObjectName("sys_time_label")
                self.train_info_label = QtWidgets.QLabel(self.centralwidget)
                self.train_info_label.setGeometry(QtCore.QRect(458, 56, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.train_info_label.setFont(font)
                self.train_info_label.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                "border: 2px solid black;\n"
                "")
                self.train_info_label.setAlignment(QtCore.Qt.AlignCenter)
                self.train_info_label.setObjectName("train_info_label")
                self.length_label = QtWidgets.QLabel(self.centralwidget)
                self.length_label.setGeometry(QtCore.QRect(458, 82, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.length_label.setFont(font)
                self.length_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.length_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.length_label.setObjectName("length_label")
                self.width_label = QtWidgets.QLabel(self.centralwidget)
                self.width_label.setGeometry(QtCore.QRect(458, 108, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.width_label.setFont(font)
                self.width_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.width_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.width_label.setObjectName("width_label")
                self.mass_label = QtWidgets.QLabel(self.centralwidget)
                self.mass_label.setGeometry(QtCore.QRect(458, 160, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.mass_label.setFont(font)
                self.mass_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.mass_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.mass_label.setObjectName("mass_label")
                self.height_label = QtWidgets.QLabel(self.centralwidget)
                self.height_label.setGeometry(QtCore.QRect(458, 134, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.height_label.setFont(font)
                self.height_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.height_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.height_label.setObjectName("height_label")
                self.temperature_label = QtWidgets.QLabel(self.centralwidget)
                self.temperature_label.setGeometry(QtCore.QRect(458, 212, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.temperature_label.setFont(font)
                self.temperature_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.temperature_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.temperature_label.setObjectName("temperature_label")
                self.passenger_label = QtWidgets.QLabel(self.centralwidget)
                self.passenger_label.setGeometry(QtCore.QRect(458, 186, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.passenger_label.setFont(font)
                self.passenger_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.passenger_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.passenger_label.setObjectName("passenger_label")
                self.temperature_spnbx = QtWidgets.QSpinBox(self.centralwidget)
                self.temperature_spnbx.setGeometry(QtCore.QRect(610, 214, 42, 22))
                self.temperature_spnbx.setObjectName("temperature_spnbx")
                self.force_label = QtWidgets.QLabel(self.centralwidget)
                self.force_label.setGeometry(QtCore.QRect(12, 58, 435, 35))
                font = QtGui.QFont()
                font.setPointSize(16)
                font.setBold(True)
                font.setWeight(75)
                self.force_label.setFont(font)
                self.force_label.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                "border: 2px solid black;\n"
                "")
                self.force_label.setAlignment(QtCore.Qt.AlignCenter)
                self.force_label.setObjectName("force_label")
                # self.force_info_label_2 = QtWidgets.QLabel(self.centralwidget)
                # self.force_info_label_2.setGeometry(QtCore.QRect(12, 92, 435, 35))
                # font = QtGui.QFont()
                # font.setPointSize(14)
                # font.setBold(True)
                # font.setWeight(75)
                # self.force_info_label_2.setFont(font)
                # self.force_info_label_2.setStyleSheet("background-color: rgb(202, 202, 202);\n"
                # "border: 1px solid black;\n"
                # "")
                # self.force_info_label_2.setAlignment(QtCore.Qt.AlignCenter)
                # self.force_info_label_2.setObjectName("force_info_label_2")

                self.force_info_label_2 = QtWidgets.QTableWidget(self.centralwidget)
                self.force_info_label_2.setGeometry(QtCore.QRect(12, 92, 435, 35))
                self.force_info_label_2.setColumnCount(2)
                self.force_info_label_2.setRowCount(1)
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.force_info_label_2.setFont(font)
                self.force_info_label_2.horizontalHeader().setVisible(False)
                self.force_info_label_2.verticalHeader().setVisible(False)
                self.force_info_label_2.verticalScrollBar().setVisible(False)
                self.force_info_label_2.setStyleSheet("background-color: rgb(202, 202, 202);\n"
                "border: 1px solid black;\n"
                "")
                self.force_info_label_2.resizeRowsToContents()
                self.force_info_label_2.setShowGrid(False)  # Remove grid lines
                self.force_info_label_2.setColumnWidth(0, 216)  # Set the width of the first column to 200 pixels
                self.force_info_label_2.setColumnWidth(1, 216)  # Set the width of the second column to 235 pixels
                self.force_info_label_2.setObjectName("force_info_label_2")

                self.velocity_label = QtWidgets.QLabel(self.centralwidget)
                self.velocity_label.setGeometry(QtCore.QRect(12, 138, 435, 35))
                font = QtGui.QFont()
                font.setPointSize(16)
                font.setBold(True)
                font.setWeight(75)
                self.velocity_label.setFont(font)
                self.velocity_label.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                "border: 2px solid black;\n"
                "")
                self.velocity_label.setAlignment(QtCore.Qt.AlignCenter)
                self.velocity_label.setObjectName("velocity_label")
                self.vacc_info_label = QtWidgets.QLabel(self.centralwidget)
                self.vacc_info_label.setGeometry(QtCore.QRect(12, 172, 435, 35))
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.vacc_info_label.setFont(font)
                self.vacc_info_label.setStyleSheet("background-color: rgb(202, 202, 202);\n"
                "border: 1px solid black;\n"
                "")
                self.vacc_info_label.setAlignment(QtCore.Qt.AlignCenter)
                self.vacc_info_label.setObjectName("vacc_info_label")
                self.accel_info_label = QtWidgets.QLabel(self.centralwidget)
                self.accel_info_label.setGeometry(QtCore.QRect(12, 286, 435, 35))
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.accel_info_label.setFont(font)
                self.accel_info_label.setStyleSheet("background-color: rgb(202, 202, 202);\n"
                "border: 1px solid black;\n"
                "")
                self.accel_info_label.setAlignment(QtCore.Qt.AlignCenter)
                self.accel_info_label.setObjectName("accel_info_label")
                self.acceleration_label = QtWidgets.QLabel(self.centralwidget)
                self.acceleration_label.setGeometry(QtCore.QRect(12, 252, 435, 35))
                font = QtGui.QFont()
                font.setPointSize(16)
                font.setBold(True)
                font.setWeight(75)
                self.acceleration_label.setFont(font)
                self.acceleration_label.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                "border: 2px solid black;\n"
                "")
                self.acceleration_label.setAlignment(QtCore.Qt.AlignCenter)
                self.acceleration_label.setObjectName("acceleration_label")
                self.vcmd_info_label = QtWidgets.QLabel(self.centralwidget)
                self.vcmd_info_label.setGeometry(QtCore.QRect(12, 206, 435, 35))
                font = QtGui.QFont()
                font.setPointSize(14)
                font.setBold(True)
                font.setWeight(75)
                self.vcmd_info_label.setFont(font)
                self.vcmd_info_label.setStyleSheet("background-color: rgb(202, 202, 202);\n"
                "border: 1px solid black;\n"
                "")
                self.vcmd_info_label.setAlignment(QtCore.Qt.AlignCenter)
                self.vcmd_info_label.setObjectName("vcmd_info_label")
                self.ad_view1 = QLabel(self.centralwidget)
                self.ad_view1.setGeometry(10, 444, 435, 119)
                self.next_station_infobox = QtWidgets.QTableWidget(self.centralwidget)
                self.next_station_infobox.setGeometry(QtCore.QRect(12, 366, 435, 73))
                self.next_station_infobox.setColumnCount(4)
                self.next_station_infobox.setRowCount(3)
                new_row_height = 5  # Adjust the row height as needed
                for row in range(self.next_station_infobox.rowCount()):
                        self.next_station_infobox.verticalHeader().resizeSection(row, new_row_height)
                self.next_station_infobox.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                font = QtGui.QFont()
                font.setPointSize(9)
                font.setBold(True)
                font.setWeight(75)
                self.next_station_infobox.setFont(font)
                self.next_station_infobox.horizontalHeader().setVisible(False)
                self.next_station_infobox.verticalHeader().setVisible(False)
                self.next_station_infobox.verticalScrollBar().setVisible(False)
                self.next_station_infobox.resizeRowsToContents()
                self.next_station_infobox.setObjectName("next_station_table")
                self.next_station_label = QtWidgets.QLabel(self.centralwidget)
                self.next_station_label.setGeometry(QtCore.QRect(12, 332, 435, 35))
                font = QtGui.QFont()
                font.setPointSize(16)
                font.setBold(True)
                font.setWeight(75)
                self.next_station_label.setFont(font)
                self.next_station_label.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                "border: 2px solid black;\n"
                "")
                self.next_station_label.setAlignment(QtCore.Qt.AlignCenter)
                self.next_station_label.setObjectName("next_station_label")
                self.emergency_mode_label = QtWidgets.QLabel(self.centralwidget)
                self.emergency_mode_label.setGeometry(QtCore.QRect(458, 244, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.emergency_mode_label.setFont(font)
                self.emergency_mode_label.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                "border: 2px solid black;\n"
                "")
                self.emergency_mode_label.setAlignment(QtCore.Qt.AlignCenter)
                self.emergency_mode_label.setObjectName("emergency_mode_label")
                self.engine_fail_label = QtWidgets.QLabel(self.centralwidget)
                self.engine_fail_label.setGeometry(QtCore.QRect(458, 296, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.engine_fail_label.setFont(font)
                self.engine_fail_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.engine_fail_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.engine_fail_label.setObjectName("engine_fail_label")
                self.signal_fail_label = QtWidgets.QLabel(self.centralwidget)
                self.signal_fail_label.setGeometry(QtCore.QRect(458, 348, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.signal_fail_label.setFont(font)
                self.signal_fail_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.signal_fail_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.signal_fail_label.setObjectName("signal_fail_label")
                self.brake_fail_label = QtWidgets.QLabel(self.centralwidget)
                self.brake_fail_label.setGeometry(QtCore.QRect(458, 322, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.brake_fail_label.setFont(font)
                self.brake_fail_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.brake_fail_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.brake_fail_label.setObjectName("brake_fail_label")
                self.ebrake_fail_label = QtWidgets.QLabel(self.centralwidget)
                self.ebrake_fail_label.setGeometry(QtCore.QRect(458, 270, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.ebrake_fail_label.setFont(font)
                self.ebrake_fail_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.ebrake_fail_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.ebrake_fail_label.setObjectName("ebrake_fail_label")
                self.ebrake_fail_off = QtWidgets.QLabel(self.centralwidget)
                self.ebrake_fail_off.setEnabled(True)
                self.ebrake_fail_off.setGeometry(QtCore.QRect(626, 274, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.ebrake_fail_off.setFont(font)
                self.ebrake_fail_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.ebrake_fail_off.setAlignment(QtCore.Qt.AlignCenter)
                self.ebrake_fail_off.setObjectName("ebrake_fail_off")
                self.engine_fail_off = QtWidgets.QLabel(self.centralwidget)
                self.engine_fail_off.setGeometry(QtCore.QRect(626, 300, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.engine_fail_off.setFont(font)
                self.engine_fail_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.engine_fail_off.setAlignment(QtCore.Qt.AlignCenter)
                self.engine_fail_off.setObjectName("engine_fail_off")
                self.brake_fail_off = QtWidgets.QLabel(self.centralwidget)
                self.brake_fail_off.setGeometry(QtCore.QRect(626, 328, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.brake_fail_off.setFont(font)
                self.brake_fail_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.brake_fail_off.setAlignment(QtCore.Qt.AlignCenter)
                self.brake_fail_off.setObjectName("brake_fail_off")
                self.signal_fail_off = QtWidgets.QLabel(self.centralwidget)
                self.signal_fail_off.setGeometry(QtCore.QRect(626, 352, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.signal_fail_off.setFont(font)
                self.signal_fail_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.signal_fail_off.setAlignment(QtCore.Qt.AlignCenter)
                self.signal_fail_off.setObjectName("signal_fail_off")
                self.ebrake_fail_on = QtWidgets.QLabel(self.centralwidget)
                self.ebrake_fail_on.setEnabled(True)
                self.ebrake_fail_on.setGeometry(QtCore.QRect(626, 274, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.ebrake_fail_on.setFont(font)
                self.ebrake_fail_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.ebrake_fail_on.setAlignment(QtCore.Qt.AlignCenter)
                self.ebrake_fail_on.setObjectName("ebrake_fail_on")
                self.engine_fail_on = QtWidgets.QLabel(self.centralwidget)
                self.engine_fail_on.setEnabled(True)
                self.engine_fail_on.setGeometry(QtCore.QRect(626, 300, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.engine_fail_on.setFont(font)
                self.engine_fail_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.engine_fail_on.setAlignment(QtCore.Qt.AlignCenter)
                self.engine_fail_on.setObjectName("engine_fail_on")
                self.brake_fail_on = QtWidgets.QLabel(self.centralwidget)
                self.brake_fail_on.setEnabled(True)
                self.brake_fail_on.setGeometry(QtCore.QRect(626, 328, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.brake_fail_on.setFont(font)
                self.brake_fail_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.brake_fail_on.setAlignment(QtCore.Qt.AlignCenter)
                self.brake_fail_on.setObjectName("brake_fail_on")
                self.signal_fail_on = QtWidgets.QLabel(self.centralwidget)
                self.signal_fail_on.setEnabled(True)
                self.signal_fail_on.setGeometry(QtCore.QRect(626, 352, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.signal_fail_on.setFont(font)
                self.signal_fail_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.signal_fail_on.setAlignment(QtCore.Qt.AlignCenter)
                self.signal_fail_on.setObjectName("signal_fail_on")
                self.engine_fail_chkbx = QtWidgets.QCheckBox(self.centralwidget)
                self.engine_fail_chkbx.setGeometry(QtCore.QRect(660, 302, 14, 15))
                self.engine_fail_chkbx.setText("")
                self.engine_fail_chkbx.setObjectName("engine_fail_chkbx")
                self.brake_fail_chkbx = QtWidgets.QCheckBox(self.centralwidget)
                self.brake_fail_chkbx.setGeometry(QtCore.QRect(660, 328, 14, 15))
                self.brake_fail_chkbx.setText("")
                self.brake_fail_chkbx.setObjectName("brake_fail_chkbx")
                self.signal_fail_chkbx = QtWidgets.QCheckBox(self.centralwidget)
                self.signal_fail_chkbx.setGeometry(QtCore.QRect(660, 354, 14, 15))
                self.signal_fail_chkbx.setText("")
                self.signal_fail_chkbx.setObjectName("signal_fail_chkbx")
                self.train_info_label_2 = QtWidgets.QLabel(self.centralwidget)
                self.train_info_label_2.setGeometry(QtCore.QRect(458, 380, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.train_info_label_2.setFont(font)
                self.train_info_label_2.setStyleSheet("background-color: rgb(149, 188, 242);\n"
                "border: 2px solid black;\n"
                "")
                self.train_info_label_2.setAlignment(QtCore.Qt.AlignCenter)
                self.train_info_label_2.setObjectName("train_info_label_2")
                self.left_door_label = QtWidgets.QLabel(self.centralwidget)
                self.left_door_label.setGeometry(QtCore.QRect(458, 432, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.left_door_label.setFont(font)
                self.left_door_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.left_door_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.left_door_label.setObjectName("left_door_label")
                self.external_lights_label = QtWidgets.QLabel(self.centralwidget)
                self.external_lights_label.setGeometry(QtCore.QRect(458, 484, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.external_lights_label.setFont(font)
                self.external_lights_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.external_lights_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.external_lights_label.setObjectName("external_lights_label")
                self.internal_lights_label = QtWidgets.QLabel(self.centralwidget)
                self.internal_lights_label.setGeometry(QtCore.QRect(458, 458, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.internal_lights_label.setFont(font)
                self.internal_lights_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.internal_lights_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.internal_lights_label.setObjectName("internal_lights_label")
                self.right_door_label = QtWidgets.QLabel(self.centralwidget)
                self.right_door_label.setGeometry(QtCore.QRect(458, 406, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.right_door_label.setFont(font)
                self.right_door_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.right_door_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.right_door_label.setObjectName("right_door_label")
                self.internal_lights_off = QtWidgets.QLabel(self.centralwidget)
                self.internal_lights_off.setEnabled(True)
                self.internal_lights_off.setGeometry(QtCore.QRect(626, 462, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.internal_lights_off.setFont(font)
                self.internal_lights_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.internal_lights_off.setAlignment(QtCore.Qt.AlignCenter)
                self.internal_lights_off.setObjectName("internal_lights_off")
                self.internal_lights_on = QtWidgets.QLabel(self.centralwidget)
                self.internal_lights_on.setEnabled(True)
                self.internal_lights_on.setGeometry(QtCore.QRect(626, 462, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.internal_lights_on.setFont(font)
                self.internal_lights_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.internal_lights_on.setAlignment(QtCore.Qt.AlignCenter)
                self.internal_lights_on.setObjectName("internal_lights_on")
                self.external_lights_off = QtWidgets.QLabel(self.centralwidget)
                self.external_lights_off.setEnabled(True)
                self.external_lights_off.setGeometry(QtCore.QRect(626, 488, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.external_lights_off.setFont(font)
                self.external_lights_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.external_lights_off.setAlignment(QtCore.Qt.AlignCenter)
                self.external_lights_off.setObjectName("external_lights_off")
                self.external_lights_on = QtWidgets.QLabel(self.centralwidget)
                self.external_lights_on.setEnabled(True)
                self.external_lights_on.setGeometry(QtCore.QRect(626, 488, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.external_lights_on.setFont(font)
                self.external_lights_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.external_lights_on.setAlignment(QtCore.Qt.AlignCenter)
                self.external_lights_on.setObjectName("external_lights_on")
                self.right_door_open = QtWidgets.QLabel(self.centralwidget)
                self.right_door_open.setEnabled(True)
                self.right_door_open.setGeometry(QtCore.QRect(598, 410, 53, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.right_door_open.setFont(font)
                self.right_door_open.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.right_door_open.setAlignment(QtCore.Qt.AlignCenter)
                self.right_door_open.setObjectName("right_door_open")
                self.right_door_closed = QtWidgets.QLabel(self.centralwidget)
                self.right_door_closed.setEnabled(True)
                self.right_door_closed.setGeometry(QtCore.QRect(598, 410, 53, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.right_door_closed.setFont(font)
                self.right_door_closed.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.right_door_closed.setAlignment(QtCore.Qt.AlignCenter)
                self.right_door_closed.setObjectName("right_door_closed")
                self.left_door_open = QtWidgets.QLabel(self.centralwidget)
                self.left_door_open.setEnabled(True)
                self.left_door_open.setGeometry(QtCore.QRect(598, 436, 53, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.left_door_open.setFont(font)
                self.left_door_open.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.left_door_open.setAlignment(QtCore.Qt.AlignCenter)
                self.left_door_open.setObjectName("left_door_open")
                self.left_door_closed = QtWidgets.QLabel(self.centralwidget)
                self.left_door_closed.setEnabled(True)
                self.left_door_closed.setGeometry(QtCore.QRect(598, 436, 53, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.left_door_closed.setFont(font)
                self.left_door_closed.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.left_door_closed.setAlignment(QtCore.Qt.AlignCenter)
                self.left_door_closed.setObjectName("left_door_closed")
                self.ebrake_off = QtWidgets.QLabel(self.centralwidget)
                self.ebrake_off.setEnabled(True)
                self.ebrake_off.setGeometry(QtCore.QRect(626, 514, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.ebrake_off.setFont(font)
                self.ebrake_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.ebrake_off.setAlignment(QtCore.Qt.AlignCenter)
                self.ebrake_off.setObjectName("ebrake_off")
                self.ebrake_on = QtWidgets.QLabel(self.centralwidget)
                self.ebrake_on.setEnabled(True)
                self.ebrake_on.setGeometry(QtCore.QRect(626, 514, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.ebrake_on.setFont(font)
                self.ebrake_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.ebrake_on.setAlignment(QtCore.Qt.AlignCenter)
                self.ebrake_on.setObjectName("ebrake_on")
                self.ebrake_label = QtWidgets.QLabel(self.centralwidget)
                self.ebrake_label.setGeometry(QtCore.QRect(458, 510, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.ebrake_label.setFont(font)
                self.ebrake_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.ebrake_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.ebrake_label.setObjectName("ebrake_label")
                self.ebrake_fail_chkbx = QtWidgets.QCheckBox(self.centralwidget)
                self.ebrake_fail_chkbx.setGeometry(QtCore.QRect(660, 276, 14, 15))
                self.ebrake_fail_chkbx.setText("")
                self.ebrake_fail_chkbx.setObjectName("ebrake_fail_chkbx")
                self.service_brake_label = QtWidgets.QLabel(self.centralwidget)
                self.service_brake_label.setGeometry(QtCore.QRect(458, 536, 198, 27))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.service_brake_label.setFont(font)
                self.service_brake_label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border: 1px solid black;\n"
                "")
                self.service_brake_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
                self.service_brake_label.setObjectName("service_brake_label")
                self.service_brake_on = QtWidgets.QLabel(self.centralwidget)
                self.service_brake_on.setEnabled(True)
                self.service_brake_on.setGeometry(QtCore.QRect(626, 540, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.service_brake_on.setFont(font)
                self.service_brake_on.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(0, 170, 0);")
                self.service_brake_on.setAlignment(QtCore.Qt.AlignCenter)
                self.service_brake_on.setObjectName("service_brake_on")
                self.service_brake_off = QtWidgets.QLabel(self.centralwidget)
                self.service_brake_off.setEnabled(True)
                self.service_brake_off.setGeometry(QtCore.QRect(626, 540, 25, 17))
                font = QtGui.QFont()
                font.setPointSize(10)
                font.setBold(True)
                font.setWeight(75)
                self.service_brake_off.setFont(font)
                self.service_brake_off.setStyleSheet("color: rgb(255, 255, 255);\n"
                "background-color: rgb(170, 0, 0);")
                self.service_brake_off.setAlignment(QtCore.Qt.AlignCenter)
                self.service_brake_off.setObjectName("service_brake_off")
                self.ebrake_label.raise_()
                self.title_label.raise_()
                # self.system_speed_label.raise_()
                # self.system_speed_spnbx.raise_()
                # self.sys_time_label.raise_()
                self.train_info_label.raise_()
                self.length_label.raise_()
                self.width_label.raise_()
                self.mass_label.raise_()
                self.height_label.raise_()
                self.temperature_label.raise_()
                self.passenger_label.raise_()
                # self.temperature_spnbx.raise_()
                self.force_label.raise_()
                self.force_info_label_2.raise_()
                self.velocity_label.raise_()
                self.vacc_info_label.raise_()
                self.accel_info_label.raise_()
                self.acceleration_label.raise_()
                self.vcmd_info_label.raise_()
                self.ad_view1.raise_()
                self.next_station_infobox.raise_()
                self.next_station_label.raise_()
                self.emergency_mode_label.raise_()
                self.engine_fail_label.raise_()
                self.signal_fail_label.raise_()
                self.brake_fail_label.raise_()
                self.ebrake_fail_label.raise_()
                self.ebrake_fail_off.raise_()
                self.engine_fail_off.raise_()
                self.brake_fail_off.raise_()
                self.signal_fail_off.raise_()
                self.ebrake_fail_on.raise_()
                self.engine_fail_on.raise_()
                self.brake_fail_on.raise_()
                self.signal_fail_on.raise_()
                self.ebrake_fail_on.hide()
                self.engine_fail_on.hide()
                self.brake_fail_on.hide()
                self.signal_fail_on.hide()
                self.engine_fail_chkbx.raise_()
                self.brake_fail_chkbx.raise_()
                self.signal_fail_chkbx.raise_()
                self.train_info_label_2.raise_()
                self.left_door_label.raise_()
                self.external_lights_label.raise_()
                self.internal_lights_label.raise_()
                self.right_door_label.raise_()
                self.internal_lights_off.raise_()
                self.internal_lights_on.raise_()
                self.internal_lights_on.hide()
                self.external_lights_off.raise_()
                self.external_lights_on.raise_()
                self.external_lights_on.hide()
                self.right_door_open.raise_()
                self.right_door_closed.raise_()
                self.right_door_open.hide()
                self.left_door_open.raise_()
                self.left_door_closed.raise_()
                self.left_door_open.hide()
                self.ebrake_off.raise_()
                self.ebrake_on.raise_()
                self.ebrake_on.hide()
                self.ebrake_fail_chkbx.raise_()
                self.service_brake_label.raise_()
                self.service_brake_on.raise_()
                self.service_brake_on.hide()
                self.service_brake_off.raise_()
                self.setCentralWidget(self.centralwidget)

                self.retranslateUi()
                QtCore.QMetaObject.connectSlotsByName(self)

                self._handler()

                # Set Default Values for Labels
                # Acceleration
                self.accel_info_label.setText(str(self.train_model.get_acceleration()) + " m/s^2")

                # Velocity
                self.vacc_info_label.setText(str("Vacc = " + str(self.train_model.get_actual_velocity()) + " m/s"))

                # Force
                # self.force_info_label_2.setText(str(self.train_model.get_force()) + " N")

                # Title
                self.title_label.setText(str(self.train_model.get_line() + " Line"))

                # Mass
                self.mass_label.setText(str("Mass: " + str(self.train_model.get_total_mass()) + " kg"))

                # Passenger Count
                self.passenger_label.setText(str("Passengers Onboard: " + str(self.train_model.get_curr_passenger_count())))

                # Temperature
                self.temperature_label.setText(str("Car Temp.: " + str(round(self.train_model.get_temperature(),0)) + "°F      SP:"))

                # Commanded Velocity
                self.vcmd_info_label.setText(str(self.train_model.get_cmd_speed()))

                # Set Default Values for Check Boxes
                # Failure Modes
                self.ebrake_fail_chkbx.toggled.connect(
                        lambda: self.train_model.set_ebrake_failure(self.ebrake_fail_chkbx.isChecked()))
                self.engine_fail_chkbx.toggled.connect(
                        lambda: self.train_model.set_engine_failure(self.engine_fail_chkbx.isChecked()))
                self.brake_fail_chkbx.toggled.connect(
                        lambda: self.train_model.set_sbrake_failure(self.brake_fail_chkbx.isChecked()))
                self.signal_fail_chkbx.toggled.connect(
                        lambda: self.train_model.set_signal_failure(self.signal_fail_chkbx.isChecked()))

        def update(self):
                _translate = QtCore.QCoreApplication.translate

                # Acceleration
                self.accel_info_label.setText(str(round(self.train_model.get_acceleration() * 2.23694, 3)) + " mi/(h * s)")

                # Velocity
                self.vacc_info_label.setText(str("Actual Velocity = " + str(round(self.train_model.get_actual_velocity() * 2.23694, 3)) + " mph"))

                # Force
                force = QtWidgets.QTableWidgetItem(str(round(self.train_model.get_force(), 3)) + " N")
                force.setTextAlignment(QtCore.Qt.AlignCenter)
                cmd_pwr = QtWidgets.QTableWidgetItem(str(round(self.train_model.get_cmd_power()/1000, 3)) + " kWh")
                cmd_pwr.setTextAlignment(QtCore.Qt.AlignCenter)
                self.force_info_label_2.setItem(0, 0, force)
                self.force_info_label_2.setItem(0, 1, cmd_pwr)

                # Title
                self.title_label.setText(str(self.train_model.get_line() + " Line"))

                # Mass
                self.mass_label.setText(_translate("TrainModel_MainUI", "Mass: " + str(self.train_model.get_total_mass()) + " kg"))

                # Passenger Count
                self.passenger_label.setText(_translate("TrainModel_MainUI", "Passengers Onboard: " + str(self.train_model.get_curr_passenger_count())))

                # Temperature
                self.temperature_label.setText(str("Car Temp.: " + str(round(self.train_model.get_temperature(),0)) + "°F"))

                # Commanded Velocity
                self.vcmd_info_label.setText(str("CMD Speed: " + str(round(self.train_model.get_cmd_speed() * 2.23694, 3)) + " mph"))

                # Next Station Info
                # Row 1
                self.next_station_infobox.setItem(0, 0, QtWidgets.QTableWidgetItem("Current Station:"))
                self.next_station_infobox.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.train_model.get_beacon())))
                # TODO: Are we measuring authority in feet or blocks?
                self.next_station_infobox.setItem(0, 2, QtWidgets.QTableWidgetItem("Authority:"))
                self.next_station_infobox.setItem(0, 3, QtWidgets.QTableWidgetItem(str(round(self.train_model.get_authority() * 3.28084, 3)) + " ft"))
                # Row 2
                self.next_station_infobox.setItem(1, 0, QtWidgets.QTableWidgetItem("Speed Limit:"))
                self.next_station_infobox.setItem(1, 1, QtWidgets.QTableWidgetItem(str(round(self.train_model.get_speed_limit() * 2.23694, 3)) + " mph"))
                self.next_station_infobox.setItem(1, 2, QtWidgets.QTableWidgetItem("Underground:"))
                self.next_station_infobox.setItem(1, 3, QtWidgets.QTableWidgetItem(str(self.train_model.get_underground())))
                # Row 3
                self.next_station_infobox.setItem(2, 0, QtWidgets.QTableWidgetItem("Grade (°):"))
                self.next_station_infobox.setItem(2, 1, QtWidgets.QTableWidgetItem(str(self.train_model.get_grade()) + "°"))
                self.next_station_infobox.setItem(2, 2, QtWidgets.QTableWidgetItem("Elevation:"))
                self.next_station_infobox.setItem(2, 3, QtWidgets.QTableWidgetItem(str(round(self.train_model.get_elevation() * 3.28084, 3)) + " ft"))

                # Advertisements
                self.ad_view1.setPixmap(QtGui.QPixmap(self.train_model.get_advertisement()))

                # Failure Modes
                # Emergency Brake Failure
                self.ebrake_fail_on.setVisible(bool(self.train_model.get_ebrake_failure()))
                self.ebrake_fail_off.setVisible(not bool(self.train_model.get_ebrake_failure()))

                # Engine Failure
                self.engine_fail_on.setVisible(bool(self.train_model.get_engine_failure()))
                self.engine_fail_off.setVisible(not bool(self.train_model.get_engine_failure()))

                # Service Brake Failure
                self.brake_fail_on.setVisible(bool(self.train_model.get_sbrake_failure()))
                self.brake_fail_off.setVisible(not bool(self.train_model.get_sbrake_failure()))

                # Signal Failure
                self.signal_fail_on.setVisible(bool(self.train_model.get_signal_failure()))
                self.signal_fail_off.setVisible(not bool(self.train_model.get_signal_failure()))

                # Controls
                # Right Door
                self.right_door_open.setVisible(bool(self.train_model.get_right_door()))
                self.right_door_closed.setVisible(not bool(self.train_model.get_right_door()))

                # Left Door
                self.left_door_open.setVisible(bool(self.train_model.get_left_door()))
                self.left_door_closed.setVisible(not bool(self.train_model.get_left_door()))

                # Internal Lights
                self.internal_lights_on.setVisible(bool(self.train_model.get_int_lights()))
                self.internal_lights_off.setVisible(not bool(self.train_model.get_int_lights()))

                # External Lights
                self.external_lights_on.setVisible(bool(self.train_model.get_ext_lights()))
                self.external_lights_off.setVisible(not bool(self.train_model.get_ext_lights()))

                # E-Brake
                self.ebrake_on.setVisible(bool(self.train_model.get_emergency_brake()))
                self.ebrake_off.setVisible(not bool(self.train_model.get_emergency_brake()))

                # Service Brake
                self.service_brake_on.setVisible(bool(self.train_model.get_service_brake()))
                self.service_brake_off.setVisible(not bool(self.train_model.get_service_brake()))

                # Force Calculation
                self.train_model.calc_force()

                # Acceleration Calculation
                self.train_model.calc_acceleration()

                # Velocity Calculation
                self.train_model.calc_actual_velocity()

                # TODO: Deprecate this when we integrate modules
                # update the temperature
                # temp = self.temperature_spnbx.value()
                # self.train_model.set_temperature(float(temp))

                # TODO: Remove this when we have a real beacon
                self.train_model.beacon_simulate()

        def _handler(self):
                self.timer = QTimer()
                self.timer.setInterval(100)  # refreshes every time period
                self.timer.timeout.connect(self.update)
                self.timer.start()

        def retranslateUi(self):
                _translate = QtCore.QCoreApplication.translate
                self.setWindowTitle(_translate("TrainModel_MainUI", "Train Model"))
                self.title_label.setText(_translate("TrainModel_MainUI", " Train #NUM Line COLOR"))
                # self.system_speed_label.setText(_translate("TrainModel_MainUI", " System Speed"))
                # self.sys_time_label.setText(_translate("TrainModel_MainUI", "13:24:55"))
                self.train_info_label.setText(_translate("TrainModel_MainUI", "Train Information"))
                self.length_label.setText(_translate("TrainModel_MainUI", "Length: 105.6 ft"))
                self.width_label.setText(_translate("TrainModel_MainUI", "Width: 8.7 ft"))
                self.mass_label.setText(_translate("TrainModel_MainUI", "Mass: 40900 Kg"))
                self.height_label.setText(_translate("TrainModel_MainUI", "Height: 11.2 ft"))
                self.temperature_label.setText(_translate("TrainModel_MainUI", "Car Temp.: 72°F      SP:"))
                self.passenger_label.setText(_translate("TrainModel_MainUI", "Passengers Onboard: 10"))
                self.force_label.setText(_translate("TrainModel_MainUI", "         Force (N)           CMD Power (kWh)"))
                # self.force_info_label_2.setText(_translate("TrainModel_MainUI", "F = P/Vcmd"))
                self.velocity_label.setText(_translate("TrainModel_MainUI", "Actual & Commanded Velocity (m/s)"))
                self.vacc_info_label.setText(_translate("TrainModel_MainUI", "Vacc = laplace(Vacc)"))
                self.accel_info_label.setText(_translate("TrainModel_MainUI", "a = F/M"))
                self.acceleration_label.setText(_translate("TrainModel_MainUI", "Acceleration (m/s²)"))
                self.vcmd_info_label.setText(_translate("TrainModel_MainUI", "Vcmd = 100 m/s"))
        #         self.next_station_infobox.setHtml(_translate("TrainModel_MainUI", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        # "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        # "p, li { white-space: pre-wrap; }\n"
        # "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:12pt; font-weight:600; font-style:normal;\">\n"
        # "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">You are arriving at DORMONT STATION in 59 minutes.</span></p></body></html>"))
                self.next_station_label.setText(_translate("TrainModel_MainUI", "Current Station Information"))
                self.emergency_mode_label.setText(_translate("TrainModel_MainUI", "Emergency & Failure Modes"))
                self.engine_fail_label.setText(_translate("TrainModel_MainUI", "Train Engine Failure"))
                self.signal_fail_label.setText(_translate("TrainModel_MainUI", "Signal Pickup Failure"))
                self.brake_fail_label.setText(_translate("TrainModel_MainUI", "Service Brake Failure"))
                self.ebrake_fail_label.setText(_translate("TrainModel_MainUI", "E-Brake Failure"))
                self.ebrake_fail_off.setText(_translate("TrainModel_MainUI", "OFF"))
                self.engine_fail_off.setText(_translate("TrainModel_MainUI", "OFF"))
                self.brake_fail_off.setText(_translate("TrainModel_MainUI", "OFF"))
                self.signal_fail_off.setText(_translate("TrainModel_MainUI", "OFF"))
                self.ebrake_fail_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.engine_fail_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.brake_fail_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.signal_fail_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.train_info_label_2.setText(_translate("TrainModel_MainUI", "Controls"))
                self.left_door_label.setText(_translate("TrainModel_MainUI", "Left Door"))
                self.external_lights_label.setText(_translate("TrainModel_MainUI", "External Lights"))
                self.internal_lights_label.setText(_translate("TrainModel_MainUI", "Internal Lights"))
                self.right_door_label.setText(_translate("TrainModel_MainUI", "Right Door"))
                self.internal_lights_off.setText(_translate("TrainModel_MainUI", "OFF"))
                self.internal_lights_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.external_lights_off.setText(_translate("TrainModel_MainUI", "OFF"))
                self.external_lights_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.right_door_open.setText(_translate("TrainModel_MainUI", "OPEN"))
                self.right_door_closed.setText(_translate("TrainModel_MainUI", "CLOSED"))
                self.left_door_open.setText(_translate("TrainModel_MainUI", "OPEN"))
                self.left_door_closed.setText(_translate("TrainModel_MainUI", "CLOSED"))
                self.ebrake_off.setText(_translate("TrainModel_MainUI", "OFF"))
                self.ebrake_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.ebrake_label.setText(_translate("TrainModel_MainUI", "E-Brake"))
                self.service_brake_label.setText(_translate("TrainModel_MainUI", "Service Brake"))
                self.service_brake_on.setText(_translate("TrainModel_MainUI", "ON"))
                self.service_brake_off.setText(_translate("TrainModel_MainUI", "OFF"))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    e = Ui_TrainModel_MainUI(TrainModel(TrainModelTrainControllerAPI()))
    # TrainModel_MainUI = QtWidgets.QMainWindow()
    # tm = TrainModel()
    # ui = Ui_self(tm)
    # ui.setupUi(TrainModel_MainUI)
    # TrainModel_MainUI.show()
    sys.exit(app.exec_())
