from PyQt5 import QtCore, QtGui, QtWidgets
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsPathItem, QGridLayout
from PyQt5.QtGui import QPen, QBrush, QColor, QTransform, QCursor
from PyQt5.QtCore import Qt
from api.track_model_train_model_api import TrackModelTrainModelAPI, Trainz
from api.track_controller_track_model_api import TrackControllerTrackModelAPI
from track_model.track_model import TrackModel
from track_model.custom_graphics_view import CustomGraphicsScene
from pylint import pyreverse
from track_model.block_info import block_info
import pandas as pd




class DiagonalLabel(QLabel):
    def __init__(self, text, angle, parent=None):
        super().__init__(text, parent)
        transform = QTransform()
        transform.rotate(angle)
        self.setTransform(transform)

class Ui_MainWindow(QMainWindow):
    def __init__(self, track_model: TrackModel) -> None:
        super().__init__()
        self.track_model = track_model
        self._filepath = ""
        self.line_picked = ''
        self.block_data = {}
        self.red_data = {}
        self.green_data = {}

        self.setupUi()
        self.show()




    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1143, 938)
        self.trackmodel_main = QtWidgets.QWidget(self)
        self.trackmodel_main.setObjectName("trackmodel_main")

        # self.scene = CustomGraphicsScene()
        # self.scene.setSceneRect(0, 61, 1142, 620)
        # self.graph_view = QtWidgets.QGraphicsView(self.scene, self.trackmodel_main)
        # self.graph_view.setGeometry(QtCore.QRect(0, 61, 1142, 620))

        # self.track_heater.setGeometry(QtCore.QRect(1100, 700, 41, 41))
        # self.track_heater.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
        #                                 "background-color: rgb(255, 0, 0);\n"
        #                                 "border: 1px solid black;\n"
        #                                 "color: rgb(255, 255, 255)")
        # self.track_heater.setObjectName("track_heater")
        self.red_button = QtWidgets.QPushButton(self.trackmodel_main)
        self.red_button.setGeometry(QtCore.QRect(170,10,90,41))
        self.red_button.setText("Red Line")
        self.red_button.setStyleSheet("font: 87 10pt \"Arial Black\";\n" "background-color: rgb(255,255,255);\n" "border: 2px solid black;\n")
        self.red_button.clicked.connect(lambda: self.red_clicked())

        #red_button.clicked.connect(lambda: scene.add_red_path_items(path_data))


        self.green_button = QtWidgets.QPushButton(self.trackmodel_main)
        self.green_button.setGeometry(QtCore.QRect(270,10,90,41))
        self.green_button.setText("green Line")
        self.green_button.setStyleSheet("font: 87 10pt \"Arial Black\";\n" "background-color: rgb(255,255,255);\n" "border: 2px solid black;\n")
        self.green_button.clicked.connect(lambda: self.green_clicked())



        self.load_file = QtWidgets.QPushButton(self.trackmodel_main, clicked=lambda: self.browse_files())
        self.load_file.setGeometry(QtCore.QRect(600,10,60,41))
        self.load_file.setText("Load File")
        self.load_file.setStyleSheet("background-color: rgb(255,255,255);\n""border: 2px solid black;\n""font: 87 8pt \"Arial\";")

        self.block_display = QtWidgets.QLabel(self.trackmodel_main)
        self.block_display.setGeometry(QtCore.QRect(380,10,60,41))
        self.block_display.setText("")
        self.block_display.setStyleSheet("background-color: rgb(255,255,255);\n""border: 2px solid black;\n""font: 87 10pt \"Arial Black\";")
        self.block_display.setAlignment(QtCore.Qt.AlignCenter)

        self.title = QtWidgets.QLabel(self.trackmodel_main)
        self.title.setGeometry(QtCore.QRect(0, 0, 1141, 61))
        self.title.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"\n"
"border: 3px solid black;\n"
"font: 87 16pt \"Arial Black\";")
        self.title.setObjectName("title")
        self.clock = QtWidgets.QLabel(self.trackmodel_main)
        self.clock.setGeometry(QtCore.QRect(1020, 10, 111, 41))
        self.clock.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.clock.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"border: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.clock.setAlignment(QtCore.Qt.AlignCenter)
        self.clock.setObjectName("clock")
        self.static_title = QtWidgets.QLabel(self.trackmodel_main)
        self.static_title.setGeometry(QtCore.QRect(0, 680, 461, 41))
        self.static_title.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"background-color: rgb(134, 177, 255);\n"
"border: 2px solid black;")
        self.static_title.setAlignment(QtCore.Qt.AlignCenter)
        self.static_title.setObjectName("static_title")
        self.t_spd_limit = QtWidgets.QLabel(self.trackmodel_main)
        self.t_spd_limit.setGeometry(QtCore.QRect(0, 720, 141, 41))
        self.t_spd_limit.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_spd_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.t_spd_limit.setObjectName("t_spd_limit")
        self.t_block_length = QtWidgets.QLabel(self.trackmodel_main)
        self.t_block_length.setGeometry(QtCore.QRect(0, 770, 141, 41))
        self.t_block_length.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_block_length.setAlignment(QtCore.Qt.AlignCenter)
        self.t_block_length.setObjectName("t_block_length")
        self.t_grade = QtWidgets.QLabel(self.trackmodel_main)
        self.t_grade.setGeometry(QtCore.QRect(0, 820, 141, 41))
        self.t_grade.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_grade.setAlignment(QtCore.Qt.AlignCenter)
        self.t_grade.setObjectName("t_grade")
        self.t_elevation = QtWidgets.QLabel(self.trackmodel_main)
        self.t_elevation.setGeometry(QtCore.QRect(0, 870, 141, 41))
        self.t_elevation.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_elevation.setAlignment(QtCore.Qt.AlignCenter)
        self.t_elevation.setObjectName("t_elevation")

        self.yard = QtWidgets.QLabel(self.trackmodel_main)
        self.yard.setGeometry(QtCore.QRect(855,240,60,20))
        self.yard.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.yard.setAlignment(QtCore.Qt.AlignCenter)
        self.yard.setText("YARD")
        self.yard.setObjectName("yard")
        self.yard.setVisible(False)

        self.speed_limit = QtWidgets.QLabel(self.trackmodel_main)
        self.speed_limit.setGeometry(QtCore.QRect(140, 720, 71, 41))
        self.speed_limit.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.speed_limit.setText("")
        self.speed_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.speed_limit.setObjectName("speed_limit")

        self.block_length = QtWidgets.QLabel(self.trackmodel_main)
        self.block_length.setGeometry(QtCore.QRect(140, 770, 71, 41))
        self.block_length.setStyleSheet("font: 87 9pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.block_length.setText("")
        self.block_length.setAlignment(QtCore.Qt.AlignCenter)
        self.block_length.setObjectName("block_length")
        self.grade = QtWidgets.QLabel(self.trackmodel_main)
        self.grade.setGeometry(QtCore.QRect(140, 820, 71, 41))
        self.grade.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.grade.setText("")
        self.grade.setAlignment(QtCore.Qt.AlignCenter)
        self.grade.setObjectName("grade")
        self.elevation = QtWidgets.QLabel(self.trackmodel_main)
        self.elevation.setGeometry(QtCore.QRect(140, 870, 71, 41))
        self.elevation.setStyleSheet("font: 87 9pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.elevation.setText("")
        self.elevation.setAlignment(QtCore.Qt.AlignCenter)
        self.elevation.setObjectName("elevation")
        self.t_section = QtWidgets.QLabel(self.trackmodel_main)
        self.t_section.setGeometry(QtCore.QRect(250, 720, 141, 41))
        self.t_section.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_section.setAlignment(QtCore.Qt.AlignCenter)
        self.t_section.setObjectName("t_section")
        self.section = QtWidgets.QLabel(self.trackmodel_main)
        self.section.setGeometry(QtCore.QRect(390, 720, 71, 41))
        self.section.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.section.setText("")
        self.section.setAlignment(QtCore.Qt.AlignCenter)
        self.section.setObjectName("section")
        self.t_swtch_pos = QtWidgets.QLabel(self.trackmodel_main)
        self.t_swtch_pos.setGeometry(QtCore.QRect(250, 770, 141, 41))
        self.t_swtch_pos.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_swtch_pos.setAlignment(QtCore.Qt.AlignCenter)
        self.t_swtch_pos.setObjectName("t_swtch_pos")
        self.t_occupied = QtWidgets.QLabel(self.trackmodel_main)
        self.t_occupied.setGeometry(QtCore.QRect(250, 820, 141, 41))
        self.t_occupied.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_occupied.setAlignment(QtCore.Qt.AlignCenter)
        self.t_occupied.setObjectName("t_occupied")
        self.t_undr = QtWidgets.QLabel(self.trackmodel_main)
        self.t_undr.setGeometry(QtCore.QRect(250, 870, 141, 41))
        self.t_undr.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_undr.setAlignment(QtCore.Qt.AlignCenter)
        self.t_undr.setObjectName("t_undr")
        self.switch_position = QtWidgets.QLabel(self.trackmodel_main)
        self.switch_position.setGeometry(QtCore.QRect(390, 770, 71, 41))
        self.switch_position.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.switch_position.setText("")
        self.switch_position.setAlignment(QtCore.Qt.AlignCenter)
        self.switch_position.setObjectName("switch_position")
        self.occupancy = QtWidgets.QLabel(self.trackmodel_main)
        self.occupancy.setGeometry(QtCore.QRect(390, 820, 71, 41))
        self.occupancy.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.occupancy.setText("")
        self.occupancy.setAlignment(QtCore.Qt.AlignCenter)
        self.occupancy.setObjectName("occupancy")
        self.underground = QtWidgets.QLabel(self.trackmodel_main)
        self.underground.setGeometry(QtCore.QRect(390, 870, 71, 41))
        self.underground.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.underground.setText("")
        self.underground.setAlignment(QtCore.Qt.AlignCenter)
        self.underground.setObjectName("underground")
        self.static_title_2 = QtWidgets.QLabel(self.trackmodel_main)
        self.static_title_2.setGeometry(QtCore.QRect(460, 680, 241, 41))
        self.static_title_2.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"background-color: rgb(134, 177, 255);\n"
"border: 2px solid black;")
        self.static_title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.static_title_2.setObjectName("static_title_2")
        self.static_title_3 = QtWidgets.QLabel(self.trackmodel_main)
        self.static_title_3.setGeometry(QtCore.QRect(700, 680, 441, 41))
        self.static_title_3.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"background-color: rgb(134, 177, 255);\n"
"border: 2px solid black;")
        self.static_title_3.setAlignment(QtCore.Qt.AlignCenter)
        self.static_title_3.setObjectName("static_title_3")
        self.line = QtWidgets.QFrame(self.trackmodel_main)
        self.line.setGeometry(QtCore.QRect(450, 720, 20, 191))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        self.line.setPalette(palette)
        self.line.setStyleSheet("")
        self.line.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line.setLineWidth(0)
        self.line.setMidLineWidth(4)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.trackmodel_main)
        self.line_2.setGeometry(QtCore.QRect(690, 720, 20, 191))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        self.line_2.setPalette(palette)
        self.line_2.setStyleSheet("")
        self.line_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.line_2.setLineWidth(0)
        self.line_2.setMidLineWidth(4)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setObjectName("line_2")
        self.t_station = QtWidgets.QLabel(self.trackmodel_main)
        self.t_station.setGeometry(QtCore.QRect(460, 720, 151, 41))
        self.t_station.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_station.setAlignment(QtCore.Qt.AlignCenter)
        self.t_station.setObjectName("t_station")
        self.station = QtWidgets.QLabel(self.trackmodel_main)
        self.station.setGeometry(QtCore.QRect(610, 720, 81, 41))
        self.station.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.station.setText("")
        self.station.setAlignment(QtCore.Qt.AlignCenter)
        self.station.setObjectName("station")
        self.t_station_name = QtWidgets.QLabel(self.trackmodel_main)
        self.t_station_name.setGeometry(QtCore.QRect(460, 770, 241, 41))
        self.t_station_name.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_station_name.setAlignment(QtCore.Qt.AlignCenter)
        self.t_station_name.setObjectName("t_station_name")
        self.station_name = QtWidgets.QLabel(self.trackmodel_main)
        self.station_name.setGeometry(QtCore.QRect(460, 810, 241, 101))
        self.station_name.setStyleSheet("font: 87 11pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 2px solid black;")
        self.station_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.station_name.setText("")
        self.station_name.setAlignment(QtCore.Qt.AlignCenter)
        self.station_name.setObjectName("station_name")
        self.t_pwr_fail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_pwr_fail.setGeometry(QtCore.QRect(700, 720, 161, 41))
        self.t_pwr_fail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_pwr_fail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_pwr_fail.setObjectName("t_pwr_fail")
        self.t_circ_fail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_circ_fail.setGeometry(QtCore.QRect(700, 790, 161, 41))
        self.t_circ_fail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_circ_fail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_circ_fail.setObjectName("t_circ_fail")
        self.t_broke_rail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_broke_rail.setGeometry(QtCore.QRect(940, 790, 161, 41))
        self.t_broke_rail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_broke_rail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_broke_rail.setObjectName("t_broke_rail")
        self.power_failure = QtWidgets.QPushButton(self.trackmodel_main)
        self.power_failure.setGeometry(QtCore.QRect(860, 720, 41, 41))
        self.power_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.power_failure.setObjectName("power_failure")
        self.broken_rail = QtWidgets.QPushButton(self.trackmodel_main)
        self.broken_rail.setGeometry(QtCore.QRect(1100, 790, 41, 41))
        self.broken_rail.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.broken_rail.setObjectName("broken_rail")
        self.circuit_failure = QtWidgets.QPushButton(self.trackmodel_main)
        self.circuit_failure.setGeometry(QtCore.QRect(860, 790, 41, 41))
        self.circuit_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.circuit_failure.setObjectName("circuit_failure")
        self.t_heater_fail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_heater_fail.setGeometry(QtCore.QRect(940, 720, 161, 41))
        self.t_heater_fail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_heater_fail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_heater_fail.setObjectName("t_heater_fail")
        self.track_heater = QtWidgets.QPushButton(self.trackmodel_main)
        self.track_heater.setGeometry(QtCore.QRect(1100, 720, 41, 41))
        self.track_heater.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.track_heater.setObjectName("track_heater")
        self.t_temp_control = QtWidgets.QLabel(self.trackmodel_main)
        self.t_temp_control.setGeometry(QtCore.QRect(680, 10, 321, 41))
        self.t_temp_control.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.t_temp_control.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"border: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.t_temp_control.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.t_temp_control.setObjectName("t_temp_control")
        self.temp_control = QtWidgets.QDoubleSpinBox(self.trackmodel_main)
        self.temp_control.setGeometry(QtCore.QRect(930, 10, 71, 41))
        self.temp_control.setStyleSheet("border: 2px solid black;")
        self.temp_control.setObjectName("temp_control")

        # ----- MAP ----- #

        self.red_map = QtWidgets.QTableWidget(self.trackmodel_main)
        self.red_map.setRowCount(13)
        self.red_map.setColumnCount(13)
        self.red_map.setGeometry(QtCore.QRect(80,185,980,315))
        self.red_map.resizeRowsToContents()
        self.red_map.setShowGrid(False)  # Remove grid lines
        self.red_map.horizontalHeader().setVisible(False)
        self.red_map.verticalHeader().setVisible(False)
        for i in range(13):
            for j in range(13):
                if i * 13 + j + 1 > 76:
                    break
                else:
                    button_text = f'{i * 13 + j + 1}'
                    button = QPushButton(button_text, self.trackmodel_main)
                    self.red_map.setCellWidget(i, j, button)
                    button.clicked.connect(self.on_button_click)
        self.red_map.resizeColumnsToContents()
        self.red_map.setVisible(False)

        self.green_map = QtWidgets.QTableWidget(self.trackmodel_main)
        self.green_map.setRowCount(13)
        self.green_map.setColumnCount(13)
        self.green_map.setGeometry(QtCore.QRect(80,185,980,315))
        self.green_map.resizeRowsToContents()
        self.green_map.setShowGrid(False)  # Remove grid lines
        self.green_map.horizontalHeader().setVisible(False)
        self.green_map.verticalHeader().setVisible(False)
        for i in range(13):
            for j in range(13):
                if i * 13 + j + 1 > 150:
                    break
                else:
                    button_text = f'{i * 13 + j + 1}'
                    button = QPushButton(button_text, self.trackmodel_main)
                    self.green_map.setCellWidget(i, j, button)
                    button.clicked.connect(self.on_button_click)
        self.green_map.resizeColumnsToContents()
        self.green_map.setVisible(False)


        self.title.raise_()
        self.clock.raise_()
        self.static_title.raise_()
        self.t_spd_limit.raise_()
        self.t_block_length.raise_()
        self.t_grade.raise_()
        self.t_elevation.raise_()
        self.speed_limit.raise_()
        self.block_length.raise_()
        self.grade.raise_()
        self.elevation.raise_()
        self.t_section.raise_()
        self.section.raise_()
        self.t_swtch_pos.raise_()
        self.t_occupied.raise_()
        self.t_undr.raise_()
        self.switch_position.raise_()
        self.occupancy.raise_()
        self.underground.raise_()
        self.static_title_2.raise_()
        self.static_title_3.raise_()
        self.t_station.raise_()
        self.station.raise_()
        self.t_station_name.raise_()
        self.station_name.raise_()
        self.t_pwr_fail.raise_()
        self.t_circ_fail.raise_()
        self.t_broke_rail.raise_()
        self.line_2.raise_()
        self.line.raise_()
        self.power_failure.raise_()
        self.broken_rail.raise_()
        self.circuit_failure.raise_()
        self.t_heater_fail.raise_()
        self.track_heater.raise_()
        self.t_temp_control.raise_()
        self.temp_control.raise_()
        self.load_file.raise_()
        self.block_display.raise_()
        self.setCentralWidget(self.trackmodel_main)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1143, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.red_button.raise_()
        self.green_button.raise_()
        self.yard.raise_()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self._handler()

    def update(self):
        _translate = QtCore.QCoreApplication.translate

        #self.clock.setText(self.track_model.get_time())
        self.track_model.set_filepath(self._filepath)

    def red_clicked(self):
        self.line_picked = 'red'
        self.green_map.setVisible(False)
        self.red_map.setVisible(True)

    def green_clicked(self):
        self.line_picked = 'green'
        self.red_map.setVisible(False)
        self.green_map.setVisible(True)

    def on_button_click(self):
        sender = self.sender()
        bnum = int(sender.text())

        if self.line_picked == 'red' and self.red_data != {}:
            info = self.red_data[bnum]
        elif self.line_picked == 'green' and self.green_data != {}:
            info = self.green_data[bnum]
        else:
            info = None

        if info is not None:
            self.speed_limit.setText(str(info['speed limit']))
            self.block_length.setText(str(info['length']))
            self.section.setText(str(info['section']))
            self.block_display.setText(sender.text())
            self.grade.setText(str(info['grade']))
            self.elevation.setText(str(info['elevation']))
            self.underground.setText(str(info['underground']))
            self.switch_position.setText(str(info['switch position']))
            if str(info['beacon']) != "nan":
                self.station_name.setText(str(info['beacon']))
                self.station.setText("Yes")
            else:
                pass



    def _handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)  # refreshes every time period
        self.timer.timeout.connect(self.update)
        self.timer.start()
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Track Model"))
        self.title.setText(_translate("MainWindow", "Track Map"))
        self.clock.setText(_translate("MainWindow", "13:24:55"))

        self.static_title.setText(_translate("MainWindow", "Static Variables"))
        self.t_spd_limit.setText(_translate("MainWindow", "Speed Limit (mph)"))
        self.t_block_length.setText(_translate("MainWindow", "Block Length (ft)"))
        self.t_grade.setText(_translate("MainWindow", "Grade (%)"))
        self.t_elevation.setText(_translate("MainWindow", "Elevation (ft)"))
        self.t_section.setText(_translate("MainWindow", "Section"))
        self.t_swtch_pos.setText(_translate("MainWindow", "Switch Position"))
        self.t_occupied.setText(_translate("MainWindow", "Occupied"))
        self.t_undr.setText(_translate("MainWindow", "Underground"))
        self.static_title_2.setText(_translate("MainWindow", "Beacon Information"))
        self.static_title_3.setText(_translate("MainWindow", "Failure Modes"))
        self.t_station.setText(_translate("MainWindow", "Station?"))
        self.t_station_name.setText(_translate("MainWindow", "Station Name"))
        self.t_pwr_fail.setText(_translate("MainWindow", "Power Failure"))
        self.t_circ_fail.setText(_translate("MainWindow", "Circuit Failure"))
        self.t_broke_rail.setText(_translate("MainWindow", "Broken Rail"))
        self.power_failure.setText(_translate("MainWindow", "Off"))
        self.broken_rail.setText(_translate("MainWindow", "Off"))
        self.circuit_failure.setText(_translate("MainWindow", "Off"))
        self.t_heater_fail.setText(_translate("MainWindow", "Track Heater Failure"))
        self.track_heater.setText(_translate("MainWindow", "Off"))
        self.t_temp_control.setText(_translate("MainWindow", "Temperature Control"))

    def browse_files(self):
        browse = QFileDialog.getOpenFileName(self.load_file)
        self._filepath = (browse[0])
        self.block_data = block_info(self._filepath)
        self.red_data = self.block_data.get_all_blocks_for_line('red')
        self.green_data = self.block_data.get_all_blocks_for_line('green')






    # def add_green(self):
    #     self.scene.clear()
    #     green_pen = QPen(Qt.green)
    #     green_pen.setWidth(5)
    #     green_pen_2 = QPen(QColor(0, 200, 0))
    #     green_pen_2.setWidth(5)
    #
    #     self.yard.setVisible(True)
    #
    #     self.p_data = [
    #         {
    #             'start': QPointF(445, 85),
    #             'points': [QPointF(445,85), QPointF(460,105)],              #A
    #             'label': "1"
    #         },
    #         {
    #             'start': QPointF(460,105),
    #             'points': [QPointF(460,105), QPointF(475, 125)],
    #             'label': "2"
    #         },
    #         {
    #             'start': QPointF(475,125),
    #             'points': [QPointF(475,125), QPointF(490, 145)],
    #             'label': "3"
    #         },
    #         {
    #             'start': QPointF(490,145),
    #             'points': [QPointF(490,145), QPointF(515,155)],             #B
    #             'label': "4"
    #         },
    #         {
    #             'start': QPointF(515,155),
    #             'points': [QPointF(515,155), QPointF(540,165)],
    #             'label': "5"
    #         },
    #         {
    #             'start': QPointF(540,165),
    #             'points': [QPointF(540,165), QPointF(565, 175)],
    #             'label': "6"
    #         },
    #         {
    #             'start': QPointF(565,175),
    #             'points': [QPointF(565,175), QPointF(605,155)],             #C
    #             'label': "7"
    #         },
    #         {
    #             'start': QPointF(605,155),
    #             'points': [QPointF(605,155), QPointF(645, 135)],
    #             'label': "8"
    #         },
    #         {#200, 50 ---- 50, 15, 15, 10, 10
    #             'start': QPointF(645,135),
    #             'points': [QPointF(645,135), QPointF(595,120)],
    #             'label': "9"
    #         },
    #         {
    #             'start': QPointF(595,120),
    #             'points': [QPointF(595,120), QPointF(545, 105)],
    #             'label': "10"
    #         },
    #         {
    #             'start': QPointF(545,105),
    #             'points': [QPointF(545,105), QPointF(495, 95)],
    #             'label': "11"
    #         },
    #         {
    #             'start': QPointF(495,95),
    #             'points': [QPointF(495,95), QPointF(445, 85)],
    #             'label': "12"
    #         },
    #         {
    #             'start': QPointF(445,85),
    #             'points': [QPointF(445,85), QPointF(425,87)],               #D
    #             'label': "13"
    #         },
    #         {
    #             'start': QPointF(425,87),
    #             'points': [QPointF(425,87), QPointF(405,89)],
    #             'label': "14"
    #         },
    #         {
    #             'start': QPointF(405,89),
    #             'points': [QPointF(405,89), QPointF(385, 91)],
    #             'label': "15"
    #         },
    #         {
    #             'start': QPointF(385,91),
    #             'points': [QPointF(385,91), QPointF(365, 93)],
    #             'label': "16"
    #         },
    #         {
    #             'start': QPointF(365,93),
    #             'points': [QPointF(365,93), QPointF(335, 110)],             #E
    #             'label': "17"
    #         },
    #         {
    #             'start': QPointF(335,110),
    #             'points': [QPointF(335,110), QPointF(305, 125)],
    #             'label': "18"
    #         },
    #         {
    #             'start': QPointF(305,125),
    #             'points': [QPointF(305,125), QPointF(290, 140)],
    #             'label': "19"
    #         },
    #         {
    #             'start': QPointF(290,140),
    #             'points': [QPointF(290,140), QPointF(285, 155)],
    #             'label': "20"
    #         },
    #         {
    #             'start': QPointF(285,155),
    #             'points': [QPointF(285,155), QPointF(285,167)],             #F
    #             'label': "21"
    #         },
    #         {
    #             'start': QPointF(285,167),
    #             'points': [QPointF(285,167), QPointF(285,179)],
    #             'label': "22"
    #         },
    #         {
    #             'start': QPointF(285,179),
    #             'points': [QPointF(285,179), QPointF(285,191)],
    #             'label': "23"
    #         },
    #         {
    #             'start': QPointF(285,191),
    #             'points': [QPointF(285,191), QPointF(285,203)],
    #             'label': "24"
    #         },
    #         {
    #             'start': QPointF(285,203),
    #             'points': [QPointF(285,203), QPointF(285, 215)],
    #             'label': "25"
    #         },
    #         {
    #             'start': QPointF(285, 215),
    #             'points': [QPointF(285, 215), QPointF(285, 227)],
    #             'label': "26"
    #         },
    #         {
    #             'start': QPointF(285, 227),
    #             'points': [QPointF(285, 227), QPointF(285, 239)],
    #             'label': "27"
    #         },
    #         {
    #             'start': QPointF(285, 239),
    #             'points': [QPointF(285, 239), QPointF(285, 251)],
    #             'label': "28"
    #         },
    #         {
    #             'start': QPointF(285, 251),
    #             'points': [QPointF(285, 251), QPointF(285, 263)],           #G
    #             'label': "29"
    #         },
    #         {
    #             'start': QPointF(285, 263),
    #             'points': [QPointF(285, 263), QPointF(285, 275)],
    #             'label': "30"
    #         },
    #         {
    #             'start': QPointF(285, 275),
    #             'points': [QPointF(285, 275), QPointF(285, 287)],
    #             'label': "31"
    #         },
    #         {
    #             'start': QPointF(285, 287),
    #             'points': [QPointF(285, 287), QPointF(285, 299)],
    #             'label': "32"
    #         },
    #         {
    #             'start': QPointF(285, 299),
    #             'points': [QPointF(285, 299), QPointF(300, 315)],           #H
    #             'label': "33"
    #         },
    #         {
    #             'start': QPointF(300, 315),
    #             'points': [QPointF(300, 315), QPointF(315, 325)],
    #             'label': "34"
    #         },
    #         {
    #             'start': QPointF(315,325),
    #             'points': [QPointF(315,325), QPointF(330,335)],
    #             'label': "35"
    #         },
    #         {
    #             'start': QPointF(330,335),
    #             'points': [QPointF(330,335), QPointF(350,335)],             #I
    #             'label': "36"
    #         },
    #         {
    #             'start': QPointF(350, 335),
    #             'points': [QPointF(350, 335), QPointF(370, 335)],
    #             'label': "37"
    #         },
    #         {
    #             'start': QPointF(370, 335),
    #             'points': [QPointF(370, 335), QPointF(390, 335)],
    #             'label': "38"
    #         },
    #         {
    #             'start': QPointF(390, 335),
    #             'points': [QPointF(390, 335), QPointF(410, 335)],
    #             'label': "39"
    #         },
    #         {
    #             'start': QPointF(410, 335),
    #             'points': [QPointF(410, 335), QPointF(430, 335)],
    #             'label': "40"
    #         },
    #         {
    #             'start': QPointF(430, 335),
    #             'points': [QPointF(430, 335), QPointF(450, 335)],
    #             'label': "41"
    #         },
    #         {
    #             'start': QPointF(450, 335),
    #             'points': [QPointF(450, 335), QPointF(470, 335)],
    #             'label': "42"
    #         },
    #         {
    #             'start': QPointF(470, 335),
    #             'points': [QPointF(470, 335), QPointF(490, 335)],
    #             'label': "43"
    #         },
    #         {
    #             'start': QPointF(490, 335),
    #             'points': [QPointF(490, 335), QPointF(510, 335)],
    #             'label': "44"
    #         },
    #         {
    #             'start': QPointF(510, 335),
    #             'points': [QPointF(510, 335), QPointF(530, 335)],
    #             'label': "45"
    #         },
    #         {
    #             'start': QPointF(530, 335),
    #             'points': [QPointF(530, 335), QPointF(550, 335)],
    #             'label': "46"
    #         },
    #         {
    #             'start': QPointF(550, 335),
    #             'points': [QPointF(550, 335), QPointF(570, 335)],
    #             'label': "47"
    #         },
    #         {
    #             'start': QPointF(570, 335),
    #             'points': [QPointF(570, 335), QPointF(590, 335)],
    #             'label': "48"
    #         },
    #         {
    #             'start': QPointF(590, 335),
    #             'points': [QPointF(590, 335), QPointF(610, 335)],
    #             'label': "49"
    #         },
    #         {
    #             'start': QPointF(610, 335),
    #             'points': [QPointF(610, 335), QPointF(630, 335)],
    #             'label': "50"
    #         },
    #         {
    #             'start': QPointF(630, 335),
    #             'points': [QPointF(630, 335), QPointF(650, 335)],
    #             'label': "51"
    #         },
    #         {
    #             'start': QPointF(650, 335),
    #             'points': [QPointF(650, 335), QPointF(670, 335)],
    #             'label': "52"
    #         },
    #         {
    #             'start': QPointF(670, 335),
    #             'points': [QPointF(670, 335), QPointF(690, 335)],
    #             'label': "53"
    #         },
    #         {
    #             'start': QPointF(690, 335),
    #             'points': [QPointF(690, 335), QPointF(710, 335)],
    #             'label': "54"
    #         },
    #         {
    #             'start': QPointF(710, 335),
    #             'points': [QPointF(710, 335), QPointF(730, 335)],
    #             'label': "55"
    #         },
    #         {
    #             'start': QPointF(730, 335),
    #             'points': [QPointF(730, 335), QPointF(750, 335)],
    #             'label': "56"
    #         },
    #         {
    #             'start': QPointF(750, 335),
    #             'points': [QPointF(750, 335), QPointF(770, 335)],
    #             'label': "57"
    #         },
    #         {
    #             'start': QPointF(770,335),
    #             'points': [QPointF(770,335), QPointF(810,345)],              #J
    #             'label': "58"
    #         },
    #         {
    #             'start': QPointF(810,345),
    #             'points': [QPointF(810,345), QPointF(845, 360)],
    #             'label': "59"
    #         },
    #         {
    #             'start': QPointF(845,360),
    #             'points': [QPointF(845,360), QPointF(880, 380)],
    #             'label': "60"
    #         },
    #         {
    #             'start': QPointF(880,380),
    #             'points': [QPointF(880,380), QPointF(915,405)],
    #             'label': "61"
    #         },
    #         {
    #             'start': QPointF(915,405),
    #             'points': [QPointF(915,405), QPointF(940, 425)],
    #             'label': "62"
    #         },
    #         {
    #             'start': QPointF(940,425),
    #             'points': [QPointF(940,425), QPointF(940,445)],             #K
    #             'label': "63"
    #         },
    #         {
    #             'start': QPointF(940,445),
    #             'points': [QPointF(940,445), QPointF(940,465)],
    #             'label': "64"
    #         },
    #         {
    #             'start': QPointF(940,465),
    #             'points': [QPointF(940,465), QPointF(940, 485)],
    #             'label': "65"
    #         },
    #         {
    #             'start': QPointF(940,485),
    #             'points': [QPointF(940,485), QPointF(940,505)],
    #             'label': "66"
    #         },
    #         {
    #             'start': QPointF(940,505),
    #             'points': [QPointF(940,505), QPointF(940,525)],
    #             'label': "67"
    #         },
    #         {
    #             'start': QPointF(940, 525),
    #             'points': [QPointF(940, 525), QPointF(940, 545)],
    #             'label': "68"
    #         },
    #         {
    #             'start': QPointF(940,545),
    #             'points': [QPointF(940,545), QPointF(930, 565)],            #L
    #             'label': "69"
    #         },
    #         {
    #             'start': QPointF(930,565),
    #             'points': [QPointF(930,565), QPointF(915,585)],
    #             'label': "70"
    #         },
    #         {
    #             'start': QPointF(915,585),
    #             'points': [QPointF(915,585), QPointF(895, 600)],
    #             'label': "71"
    #         },
    #         {
    #             'start': QPointF(895,600),
    #             'points': [QPointF(895,600), QPointF(855, 610)],
    #             'label': "72"
    #         },
    #         {
    #             'start': QPointF(855,610),
    #             'points': [QPointF(855,610), QPointF(815,620)],
    #             'label': "73"
    #         },
    #         {
    #             'start': QPointF(815,620),
    #             'points': [QPointF(815,620), QPointF(765,620)],             #M
    #             'label': "74"
    #         },
    #         {
    #             'start': QPointF(765,620),
    #             'points': [QPointF(765,620), QPointF(715,620)],
    #             'label': "75"
    #         },
    #         {
    #             'start': QPointF(715,620),
    #             'points': [QPointF(715,620), QPointF(665,620)],
    #             'label': "76"
    #         },
    #         {
    #             'start': QPointF(665,620),
    #             'points': [QPointF(665,620), QPointF(630,620)],             #N
    #             'label': "77"
    #         },
    #         {
    #             'start': QPointF(630, 620),
    #             'points': [QPointF(630, 620), QPointF(595, 620)],
    #             'label': "78"
    #         },
    #         {
    #             'start': QPointF(595, 620),
    #             'points': [QPointF(595, 620), QPointF(560, 620)],
    #             'label': "79"
    #         },
    #         {
    #             'start': QPointF(560, 620),
    #             'points': [QPointF(560, 620), QPointF(525, 620)],
    #             'label': "80"
    #         },
    #         {
    #             'start': QPointF(525, 620),
    #             'points': [QPointF(525, 620), QPointF(490, 620)],
    #             'label': "81"
    #         },
    #         {
    #             'start': QPointF(490, 620),
    #             'points': [QPointF(490, 620), QPointF(455, 620)],
    #             'label': "82"
    #         },
    #         {
    #             'start': QPointF(455, 620),
    #             'points': [QPointF(455, 620), QPointF(420, 620)],
    #             'label': "83"
    #         },
    #         {
    #             'start': QPointF(420, 620),
    #             'points': [QPointF(420, 620), QPointF(385, 620)],
    #             'label': "84"
    #         },
    #         {
    #             'start': QPointF(385, 620),
    #             'points': [QPointF(385, 620), QPointF(350, 620)],
    #             'label': "85"
    #         },
    #         {
    #             'start': QPointF(350,620),
    #             'points': [QPointF(350,620), QPointF(330,620)],
    #             'label': "86"
    #         },
    #         {
    #             'start': QPointF(330,620),
    #             'points': [QPointF(330,620), QPointF(310,620)],
    #             'label': "87"
    #         },
    #         {
    #             'start': QPointF(310,620),
    #             'points': [QPointF(310,620), QPointF(290,620)],
    #             'label': "88"
    #         },
    #         {
    #             'start': QPointF(290,620),
    #             'points': [QPointF(290,620), QPointF(270, 600)],            #P
    #             'label': "89"
    #         },
    #         {
    #             'start': QPointF(270,600),
    #             'points': [QPointF(270,600), QPointF(250, 580)],
    #             'label': "90"
    #         },
    #         {
    #             'start': QPointF(250,580),
    #             'points': [QPointF(250,580), QPointF(245, 560)],
    #             'label': "91"
    #         },
    #         {
    #             'start': QPointF(245,560),
    #             'points': [QPointF(245,560), QPointF(245, 540)],
    #             'label': "92"
    #         },
    #         {
    #             'start': QPointF(245,540),
    #             'points': [QPointF(245,540), QPointF(250, 520)],
    #             'label': "93"
    #         },
    #         {
    #             'start': QPointF(250,520),
    #             'points': [QPointF(250,520), QPointF(270, 500)],
    #             'label': "94"
    #         },
    #         {
    #             'start': QPointF(270,500),
    #             'points': [QPointF(270,500), QPointF(295, 505)],
    #             'label': "95"
    #         },
    #         {
    #             'start': QPointF(295,505),
    #             'points': [QPointF(295,505), QPointF(315,525)],
    #             'label': "96"
    #         },
    #         {
    #             'start': QPointF(315,525),
    #             'points': [QPointF(315,525), QPointF(320,550)],
    #             'label': "97"
    #         },
    #         {
    #             'start': QPointF(320,550),
    #             'points': [QPointF(320,550), QPointF(330,580)],             #Q
    #             'label': "98"
    #         },
    #         {
    #             'start': QPointF(330,580),
    #             'points': [QPointF(330,580), QPointF(350,605)],
    #             'label': "99"
    #         },
    #         {
    #             'start': QPointF(350,605),
    #             'points': [QPointF(350,605), QPointF(370,620)],
    #             'label': "100"
    #         },
    #         {#665,620
    #             'start': QPointF(665,620),
    #             'points': [QPointF(665,620), QPointF(690,590)],             #R
    #             'label': "101"
    #         }
    #     ]
    #
    #     for i, data in enumerate(self.p_data):
    #         path = QPainterPath()
    #         path.moveTo(data['start'])
    #         for point in data['points']:
    #             path.quadTo(point, point)
    #
    #         r = QGraphicsPathItem(path)
    #         r.setData(0, data['label'])
    #         if i % 2 == 0:
    #             r.setPen(green_pen)
    #         else:
    #             r.setPen(green_pen_2)
    #
    #         self.scene.addItem(r)



    # def add_red(self):
    #     if self.r_c:
    #         red_pen = QPen(Qt.red)
    #         red_pen.setWidth(5)
    #         red_pen_2 = QPen(QColor(200, 0, 0))
    #         red_pen_2.setWidth(5)
    #
    #         self.yard.setVisible(True)
    #
    #         self.path_data = [
    #             {
    #                 'start': QPointF(725, 220),
    #                 'points': [QPointF(725, 220), QPointF(760, 205)],  # A
    #                 'label': "1"
    #             },
    #             {
    #                 'start': QPointF(760, 205),
    #                 'points': [QPointF(760, 205), QPointF(790, 185)],
    #                 'label': "2"
    #             },
    #             {
    #                 'start': QPointF(790, 185),
    #                 'points': [QPointF(790, 185), QPointF(820, 165)],
    #                 'label': "3"
    #             },
    #             {
    #                 'start': QPointF(820, 165),
    #                 'points': [QPointF(820, 165), QPointF(840, 145)],  # B
    #                 'label': "4"
    #             },
    #             {
    #                 'start': QPointF(840, 145),
    #                 'points': [QPointF(840, 145), QPointF(860, 125)],
    #                 'label': "5"
    #             },
    #             {
    #                 'start': QPointF(860, 125),
    #                 'points': [QPointF(860, 125), QPointF(890, 115)],
    #                 'label': "6"
    #             },
    #             {
    #                 'start': QPointF(890, 115),
    #                 'points': [QPointF(890, 115), QPointF(920, 120)],  # C
    #                 'label': "7"
    #             },
    #             {
    #                 'start': QPointF(920, 120),
    #                 'points': [QPointF(920, 120), QPointF(950, 125)],
    #                 'label': "8"
    #             },
    #             {
    #                 'start': QPointF(950, 125),
    #                 'points': [QPointF(950, 125), QPointF(980, 145)],
    #                 'label': "9"
    #             },
    #             {
    #                 'start': QPointF(980, 145),  # 38, 18, 855, 220            #D
    #                 'points': [QPointF(980, 145), QPointF(935, 175)],
    #                 'label': "10"
    #             },
    #             {
    #                 'start': QPointF(935, 175),
    #                 'points': [QPointF(935, 175), QPointF(885, 200)],
    #                 'label': "11"
    #             },
    #             {
    #                 'start': QPointF(885, 200),
    #                 'points': [QPointF(885, 200), QPointF(840, 220)],
    #                 'label': "12"
    #             },
    #             {  # 725,220
    #                 'start': QPointF(840, 220),  # E
    #                 'points': [QPointF(840, 220), QPointF(805, 220)],
    #                 'label': "13"
    #             },
    #             {
    #                 'start': QPointF(805, 220),
    #                 'points': [QPointF(805, 220), QPointF(765, 220)],
    #                 'label': "14"
    #             },
    #             {
    #                 'start': QPointF(765, 220),
    #                 'points': [QPointF(765, 220), QPointF(725, 220)],
    #                 'label': "15"
    #             },
    #             {
    #                 'start': QPointF(725, 220),  # F
    #                 'points': [QPointF(725, 220), QPointF(700, 220)],
    #                 'label': "16"
    #             },
    #             {
    #                 'start': QPointF(700, 220),
    #                 'points': [QPointF(700, 220), QPointF(680, 220)],
    #                 'label': "17"
    #             },
    #             {
    #                 'start': QPointF(680, 220),
    #                 'points': [QPointF(680, 220), QPointF(660, 220)],
    #                 'label': "18"
    #             },
    #             {
    #                 'start': QPointF(660, 220),
    #                 'points': [QPointF(660, 220), QPointF(640, 220)],
    #                 'label': "19"
    #             },
    #             {
    #                 'start': QPointF(640, 220),
    #                 'points': [QPointF(640, 220), QPointF(620, 220)],
    #                 'label': "20"
    #             },
    #             {
    #                 'start': QPointF(620, 220),  # G
    #                 'points': [QPointF(620, 220), QPointF(595, 225)],
    #                 'label': "21"
    #             },
    #             {
    #                 'start': QPointF(595, 225),
    #                 'points': [QPointF(595, 225), QPointF(570, 235)],
    #                 'label': "22"
    #             },
    #             {
    #                 'start': QPointF(570, 235),
    #                 'points': [QPointF(570, 235), QPointF(545, 250)],
    #                 'label': "23"
    #             },
    #             {
    #                 'start': QPointF(545, 250),  # H
    #                 'points': [QPointF(545, 250), QPointF(545, 262)],
    #                 'label': "24"
    #             },
    #             {
    #                 'start': QPointF(545, 262),
    #                 'points': [QPointF(545, 262), QPointF(545, 274)],
    #                 'label': "25"
    #             },
    #             {
    #                 'start': QPointF(545, 274),
    #                 'points': [QPointF(545, 274), QPointF(545, 286)],
    #                 'label': "26"
    #             },
    #             {
    #                 'start': QPointF(545, 286),
    #                 'points': [QPointF(545, 286), QPointF(545, 298)],
    #                 'label': "27"
    #             },
    #             {
    #                 'start': QPointF(545, 298),
    #                 'points': [QPointF(545, 298), QPointF(545, 310)],
    #                 'label': "28"
    #             },
    #             {
    #                 'start': QPointF(545, 310),
    #                 'points': [QPointF(545, 310), QPointF(545, 322)],
    #                 'label': "29"
    #             },
    #             {
    #                 'start': QPointF(545, 322),
    #                 'points': [QPointF(545, 322), QPointF(545, 334)],
    #                 'label': "30"
    #             },
    #             {
    #                 'start': QPointF(545, 334),
    #                 'points': [QPointF(545, 334), QPointF(545, 346)],
    #                 'label': "31"
    #             },
    #             {
    #                 'start': QPointF(545, 346),
    #                 'points': [QPointF(545, 346), QPointF(545, 358)],
    #                 'label': "32"
    #             },
    #             {
    #                 'start': QPointF(545, 358),
    #                 'points': [QPointF(545, 358), QPointF(545, 370)],
    #                 'label': "33"
    #             },
    #             {
    #                 'start': QPointF(545, 370),
    #                 'points': [QPointF(545, 370), QPointF(545, 382)],
    #                 'label': "34"
    #             },
    #             {
    #                 'start': QPointF(545, 382),
    #                 'points': [QPointF(545, 382), QPointF(545, 394)],
    #                 'label': "35"
    #             },
    #             {
    #                 'start': QPointF(545, 394),
    #                 'points': [QPointF(545, 394), QPointF(545, 406)],
    #                 'label': "36"
    #             },
    #             {
    #                 'start': QPointF(545, 406),
    #                 'points': [QPointF(545, 406), QPointF(545, 418)],
    #                 'label': "37"
    #             },
    #             {
    #                 'start': QPointF(545, 418),
    #                 'points': [QPointF(545, 418), QPointF(545, 430)],
    #                 'label': "38"
    #             },
    #             {
    #                 'start': QPointF(545, 430),
    #                 'points': [QPointF(545, 430), QPointF(545, 442)],
    #                 'label': "39"
    #             },
    #             {
    #                 'start': QPointF(545, 442),
    #                 'points': [QPointF(545, 442), QPointF(545, 454)],
    #                 'label': "40"
    #             },
    #             {
    #                 'start': QPointF(545, 454),
    #                 'points': [QPointF(545, 454), QPointF(545, 466)],
    #                 'label': "41"
    #             },
    #             {
    #                 'start': QPointF(545, 466),
    #                 'points': [QPointF(545, 466), QPointF(545, 478)],
    #                 'label': "42"
    #             },
    #             {
    #                 'start': QPointF(545, 478),
    #                 'points': [QPointF(545, 478), QPointF(545, 490)],
    #                 'label': "43"
    #             },
    #             {
    #                 'start': QPointF(545, 490),
    #                 'points': [QPointF(545, 490), QPointF(545, 502)],
    #                 'label': "44"
    #             },
    #             {
    #                 'start': QPointF(545, 502),
    #                 'points': [QPointF(545, 502), QPointF(545, 514)],
    #                 'label': "45"
    #             },
    #             {
    #                 'start': QPointF(545, 514),  # I
    #                 'points': [QPointF(545, 514), QPointF(520, 545)],
    #                 'label': "46"
    #             },
    #             {
    #                 'start': QPointF(520, 545),
    #                 'points': [QPointF(520, 545), QPointF(500, 565)],
    #                 'label': "47"
    #             },
    #             {
    #                 'start': QPointF(500, 565),
    #                 'points': [QPointF(500, 565), QPointF(465, 575)],
    #                 'label': "48"
    #             },
    #             {
    #                 'start': QPointF(465, 575),  # J
    #                 'points': [QPointF(465, 575), QPointF(440, 575)],
    #                 'label': "49"
    #             },
    #             {
    #                 'start': QPointF(440, 575),
    #                 'points': [QPointF(440, 575), QPointF(415, 575)],
    #                 'label': "50"
    #             },
    #             {
    #                 'start': QPointF(415, 575),
    #                 'points': [QPointF(415, 575), QPointF(390, 575)],
    #                 'label': "51"
    #             },
    #             {
    #                 'start': QPointF(390, 575),
    #                 'points': [QPointF(390, 575), QPointF(365, 575)],
    #                 'label': "52"
    #             },
    #             {
    #                 'start': QPointF(365, 575),
    #                 'points': [QPointF(365, 575), QPointF(340, 575)],
    #                 'label': "53"
    #             },
    #             {
    #                 'start': QPointF(340, 575),
    #                 'points': [QPointF(340, 575), QPointF(315, 575)],
    #                 'label': "54"
    #             },
    #             {
    #                 'start': QPointF(315, 575),  # K
    #                 'points': [QPointF(315, 575), QPointF(290, 550)],
    #                 'label': "55"
    #             },
    #             {
    #                 'start': QPointF(290, 550),
    #                 'points': [QPointF(290, 550), QPointF(265, 520)],
    #                 'label': "56"
    #             },
    #             {
    #                 'start': QPointF(265, 520),
    #                 'points': [QPointF(265, 520), QPointF(240, 485)],
    #                 'label': "57"
    #             },
    #             {
    #                 'start': QPointF(240, 485),  # L
    #                 'points': [QPointF(240, 485), QPointF(250, 455)],
    #                 'label': "58"
    #             },
    #             {
    #                 'start': QPointF(250, 455),
    #                 'points': [QPointF(250, 455), QPointF(270, 435)],
    #                 'label': "59"
    #             },
    #             {
    #                 'start': QPointF(270, 435),
    #                 'points': [QPointF(270, 435), QPointF(290, 420)],
    #                 'label': "60"
    #             },
    #             {
    #                 'start': QPointF(290, 420),  # M
    #                 'points': [QPointF(290, 420), QPointF(320, 460)],
    #                 'label': "61"
    #             },
    #             {
    #                 'start': QPointF(320, 460),
    #                 'points': [QPointF(320, 460), QPointF(335, 510)],
    #                 'label': "62"
    #             },
    #             {
    #                 'start': QPointF(335, 510),
    #                 'points': [QPointF(335, 510), QPointF(345, 535)],
    #                 'label': "63"
    #             },
    #             {  # x = 415 | y = 575
    #                 'start': QPointF(345, 535),  # N
    #                 'points': [QPointF(345, 535), QPointF(365, 550)],
    #                 'label': "64"
    #             },
    #             {
    #                 'start': QPointF(365, 550),
    #                 'points': [QPointF(365, 550), QPointF(390, 565)],
    #                 'label': "65"
    #             },
    #             {
    #                 'start': QPointF(390, 565),
    #                 'points': [QPointF(390, 565), QPointF(415, 575)],
    #                 'label': "66"
    #             },
    #             {
    #                 'start': QPointF(542, 490),  # O
    #                 'points': [QPointF(542, 490), QPointF(507, 470)],
    #                 'label': "67"
    #             },
    #             {
    #                 'start': QPointF(507, 470),  # P
    #                 'points': [QPointF(507, 470), QPointF(507, 455)],
    #                 'label': "68"
    #             },
    #             {
    #                 'start': QPointF(507, 455),
    #                 'points': [QPointF(507, 455), QPointF(507, 440)],
    #                 'label': "69"
    #             },
    #             {
    #                 'start': QPointF(507, 440),
    #                 'points': [QPointF(507, 440), QPointF(507, 425)],
    #                 'label': "70"
    #             },
    #             {
    #                 'start': QPointF(507, 425),  # Q
    #                 'points': [QPointF(507, 425), QPointF(542, 405)],
    #                 'label': "71"
    #             },
    #             {
    #                 'start': QPointF(542, 345),  # R
    #                 'points': [QPointF(542, 345), QPointF(507, 335)],
    #                 'label': "72"
    #             },
    #             {
    #                 'start': QPointF(507, 335),  # S
    #                 'points': [QPointF(507, 335), QPointF(507, 310)],
    #                 'label': "73"
    #             },
    #             {
    #                 'start': QPointF(507, 310),
    #                 'points': [QPointF(507, 310), QPointF(507, 295)],
    #                 'label': "74"
    #             },
    #             {
    #                 'start': QPointF(507, 295),
    #                 'points': [QPointF(507, 295), QPointF(507, 280)],
    #                 'label': "75"
    #             },
    #             {
    #                 'start': QPointF(507, 280),  # T
    #                 'points': [QPointF(507, 280), QPointF(542, 260)],
    #                 'label': "76"
    #             },
    #             {
    #                 'start': QPointF(980, 145),  # YARD
    #                 'points': [QPointF(980, 145), QPointF(900, 245)],
    #                 'label': ""
    #             }
    #
    #         ]
    #
    #         for i, data in enumerate(self.path_data):
    #             path = QPainterPath()
    #             path.moveTo(data['start'])
    #             for point in data['points']:
    #                 path.quadTo(point, point)
    #
    #             r = QGraphicsPathItem(path)
    #             r.setData(0, data['label'])
    #             if i % 2 == 0:
    #                 r.setPen(red_pen)
    #             else:
    #                 r.setPen(red_pen_2)
    #
    #             self.scene.addItem(r)








if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    e = Ui_MainWindow(TrackModel(TrackControllerTrackModelAPI(), TrackModelTrainModelAPI()))

    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())
