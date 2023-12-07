import traceback

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
import random



class Ui_MainWindow(QMainWindow):
    def __init__(self, track_model: TrackModel) -> None:
        super().__init__()
        self.track_model = track_model
        self._filepath = ""

        #MAP
        self.line_picked = ''
        self.block_data = {}
        self.red_data = {}
        self.green_data = {}
        self.occupied_blocks = list()

        #FAILURES
        self.circuit_failure_detected = False
        self.power_failure_detected = False
        self.broken_rail_detected = False
        self.heater_failure_detected = False
        self.block_clicked = False
        self.failure_block = {}
        self.failure_block_selected = 0

        #LIGHTS
        self.light_list = {}
        self.light_status = 0

        #TEMPERATURE CONTROL
        self.current_temp = 0
        self.target_temp = 0



        self.environment_temp = float(random.randrange(65,75))
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
        self.red_button.setGeometry(QtCore.QRect(140,10,90,41))
        self.red_button.setText("Red Line")
        self.red_button.setStyleSheet("font: 87 10pt \"Arial Black\";\n" "background-color: rgb(255,255,255);\n" "border: 2px solid black;\n")
        self.red_button.clicked.connect(lambda: self.red_clicked())
        self.red_button.setCursor(Qt.PointingHandCursor)

        #red_button.clicked.connect(lambda: scene.add_red_path_items(path_data))


        self.green_button = QtWidgets.QPushButton(self.trackmodel_main)
        self.green_button.setGeometry(QtCore.QRect(240,10,90,41))
        self.green_button.setText("Green Line")
        self.green_button.setStyleSheet("font: 87 10pt \"Arial Black\";\n" "background-color: rgb(255,255,255);\n" "border: 2px solid black;\n")
        self.green_button.clicked.connect(lambda: self.green_clicked())
        self.green_button.setCursor(Qt.PointingHandCursor)

        self.t_direction = QtWidgets.QLabel(self.trackmodel_main)
        self.t_direction.setGeometry(QtCore.QRect(420,65,300,45))
        self.t_direction.setText("Direction")
        self.t_direction.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"background-color: rgb(134, 177, 255);\n"
"border: 2px solid black;")
        self.t_direction.setAlignment(QtCore.Qt.AlignCenter)


        self.direction = QtWidgets.QLabel(self.trackmodel_main)
        self.direction.setGeometry(QtCore.QRect(420,110,300,60))
        self.direction.setText("")
        self.direction.setStyleSheet("font: 87 16pt \"Arial Black\";\n" "background-color: rgb(255,255,255);\n" "border: 2px solid black;\n")
        self.direction.setAlignment(QtCore.Qt.AlignCenter)

        self.red_light = QtWidgets.QLabel(self.trackmodel_main)
        self.red_light.setGeometry(QtCore.QRect(230,550,80,80))
        self.red_light.setStyleSheet("background-color: rgba(255,0,0," + str(self.light_status * 180) + ");\n" "border:3px solid black;\n")

        self.green_light = QtWidgets.QLabel(self.trackmodel_main)
        self.green_light.setGeometry(QtCore.QRect(830, 550, 80, 80))
        self.green_light.setStyleSheet("background-color: rgba(0,255,0,0);\n" "border:3px solid black;\n")



        self.load_file = QtWidgets.QPushButton(self.trackmodel_main, clicked=lambda: self.browse_files())
        self.load_file.setGeometry(QtCore.QRect(340,10,80,41))
        self.load_file.setText("Load File")
        self.load_file.setStyleSheet("background-color: rgb(255,255,255);\n""border: 2px solid black;\n""font: 87 10pt \"Arial Black\";")
        self.load_file.setCursor(Qt.PointingHandCursor)

        self.title = QtWidgets.QLabel(self.trackmodel_main)
        self.title.setGeometry(QtCore.QRect(0, 0, 1141, 61))
        self.title.setStyleSheet("background-color: rgb(255, 255, 0);\n"
"\n"
"border: 3px solid black;\n"
"font: 87 16pt \"Arial Black\";")
        self.title.setObjectName("title")
#         self.clock = QtWidgets.QLabel(self.trackmodel_main)
#         self.clock.setGeometry(QtCore.QRect(1020, 10, 111, 41))
#         self.clock.setLayoutDirection(QtCore.Qt.RightToLeft)
#         self.clock.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
# "border: 2px solid black;\n"
# "background-color: rgb(255, 255, 255);")
#         self.clock.setAlignment(QtCore.Qt.AlignCenter)
#         self.clock.setObjectName("clock")
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
        self.t_station.setGeometry(QtCore.QRect(460, 815, 151, 41))
        self.t_station.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_station.setAlignment(QtCore.Qt.AlignCenter)
        self.t_station.setObjectName("t_station")
        self.station = QtWidgets.QLabel(self.trackmodel_main)
        self.station.setGeometry(QtCore.QRect(610, 815, 81, 41))
        self.station.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.station.setText("")
        self.station.setAlignment(QtCore.Qt.AlignCenter)
        self.station.setObjectName("station")

        self.block_display = QtWidgets.QLabel(self.trackmodel_main)
        self.block_display.setGeometry(QtCore.QRect(610, 860, 81, 41))
        self.block_display.setText("")
        self.block_display.setStyleSheet(
            "background-color: rgb(255,255,255);\n""border: 1px solid black;\n""font: 87 10pt \"Arial Black\";")
        self.block_display.setAlignment(QtCore.Qt.AlignCenter)

        self.t_block_display = QtWidgets.QLabel(self.trackmodel_main)
        self.t_block_display.setGeometry(QtCore.QRect(460, 860, 151, 41))
        self.t_block_display.setText("Selected Block")
        self.t_block_display.setStyleSheet("background-color: rgb(194, 194, 194);\n"
                                           "font: 87 10pt \"Arial Black\";\n"
                                           "border: 1px solid black;")

        self.t_station_name = QtWidgets.QLabel(self.trackmodel_main)
        self.t_station_name.setGeometry(QtCore.QRect(460, 720, 241, 41))
        self.t_station_name.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_station_name.setAlignment(QtCore.Qt.AlignCenter)
        self.t_station_name.setObjectName("t_station_name")
        self.station_name = QtWidgets.QLabel(self.trackmodel_main)
        self.station_name.setGeometry(QtCore.QRect(460, 760, 241, 51))
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
"background-color: rgba(255, 0, 0,20);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.power_failure.setObjectName("power_failure")
        self.power_failure.clicked.connect(self.power_failure_clicked)

        self.broken_rail = QtWidgets.QPushButton(self.trackmodel_main)
        self.broken_rail.setGeometry(QtCore.QRect(1100, 790, 41, 41))
        self.broken_rail.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgba(255, 0, 0,20);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.broken_rail.setObjectName("broken_rail")
        self.broken_rail.clicked.connect(self.broken_rail_clicked)

        self.circuit_failure = QtWidgets.QPushButton(self.trackmodel_main)
        self.circuit_failure.setGeometry(QtCore.QRect(860, 790, 41, 41))
        self.circuit_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgba(255, 0, 0,20);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.circuit_failure.setObjectName("circuit_failure")
        self.circuit_failure.clicked.connect(self.circuit_failure_clicked)

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
"background-color: rgba(255, 0, 0,20);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.track_heater.setObjectName("track_heater")
        self.track_heater.clicked.connect(self.heater_failure_clicked)

        self.t_temp_control = QtWidgets.QLabel(self.trackmodel_main)
        self.t_temp_control.setGeometry(QtCore.QRect(490, 10, 165, 41))
        self.t_temp_control.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.t_temp_control.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"border: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.t_temp_control.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.t_temp_control.setObjectName("t_temp_control")
        self.temp_control = QtWidgets.QDoubleSpinBox(self.trackmodel_main)
        self.temp_control.setGeometry(QtCore.QRect(665, 10, 71, 41))
        self.temp_control.setStyleSheet("border: 2px solid black;")
        self.temp_control.setObjectName("temp_control")
        self.temp_control.setValue(70)
        self.temp_control.valueChanged.connect(self.track_heater_control)

        self.heater_temp = QtWidgets.QLabel(self.trackmodel_main)
        self.heater_temp.setGeometry(QtCore.QRect(755,10,71,41))
        self.heater_temp.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"border: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.heater_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.heater_temp.setText("")


        self.env_temp = QtWidgets.QLabel(self.trackmodel_main)
        self.env_temp.setGeometry(QtCore.QRect(860,10,150,41))
        self.env_temp.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"border: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.env_temp.setText("Temperature")

        self.e_temp = QtWidgets.QLabel(self.trackmodel_main)
        self.e_temp.setGeometry(QtCore.QRect(1020,10,70,41))
        self.e_temp.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"border: 2px solid black;\n"
"background-color: rgb(255, 255, 255);")
        self.e_temp.setAlignment(QtCore.Qt.AlignCenter)
        self.e_temp.setText(str(self.environment_temp))


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
        # self.clock.raise_()
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
        #self.yard.raise_()
        self.t_block_display.raise_()
        self.env_temp.raise_()
        self.e_temp.raise_()
        self.red_light.raise_()
        self.green_light.raise_()
        self.heater_temp.raise_()
        self.direction.raise_()
        self.t_direction.raise_()

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self._handler()

    def update(self):
        _translate = QtCore.QCoreApplication.translate
        self.light_list = self.track_model.get_light_colors()
        self.up_temp()


        #self.clock.setText(self.track_model.get_time())
        self.track_model.set_filepath(self._filepath)
        self.occupied_blocks = self.track_model.get_current_block()
        # Access every first element in each sublist of the list
        self.occupied_blocks = [i[1] for i in self.occupied_blocks]
        try:
            self.update_map_occupancy(self.occupied_blocks)
        except Exception as e:
            print(e)





    def red_clicked(self):
        self.line_picked = 'red'
        self.green_map.setVisible(False)
        self.red_map.setVisible(True)
        self.title.setText("Red Line")
        self.clear_labels()


    def green_clicked(self):
        self.line_picked = 'green'
        self.red_map.setVisible(False)
        self.green_map.setVisible(True)
        self.title.setText("Green Line")
        self.clear_labels()

    def on_button_click(self):
        sender = self.sender()
        bnum = int(sender.text())


        if self.line_picked == 'red' and self.red_data != {}:
            info = self.red_data[bnum]
        elif self.line_picked == 'green' and self.green_data != {}:
            info = self.green_data[bnum]
            # row = int(sender.text()) // self.green_map.columnCount()
            # column = (int(sender.text()) % self.green_map.columnCount())-2
            # item = QTableWidgetItem()
            # item.setBackground(QColor(0, 0, 255))
            # self.green_map.setItem(row,column,item)
        else:
            info = None

        if info is not None:
            self.block_clicked = True
            km_hr = float(info['speed limit'])
            mi_hr = km_hr / 1.60934709
            self.speed_limit.setText(str(round(mi_hr,2)))
            m = float(info['length'])
            ft = m * 3.28084
            self.block_length.setText(str(round(ft,2)))
            self.section.setText(str(info['section']))
            self.block_display.setText(sender.text())
            self.grade.setText(str(info['grade']))
            e_m = float(info['elevation'])
            e_ft = e_m * 3.28084
            self.elevation.setText(str(round(e_ft,2)))
            self.underground.setText(str(info['underground']))
            self.switch_position.setText(str(info['switch position']))
            if str(info['beacon']) != "nan":
                self.station_name.setText(str(info['beacon']))
                self.station.setText(str(info['station side']))
            else:
                self.station_name.setText("")
                self.station.setText("")

            if int(sender.text()) in self.occupied_blocks:
                self.occupancy.setText("Yes")
            else:
                self.occupancy.setText("No")

            if sender.text() in self.light_list.keys():
                self.light_status = self.light_list[sender.text()]
                if self.light_status == 1:
                    self.red_light.setStyleSheet("background-color: rgba(255,0,0,0);\n" "border:3px solid black;\n")
                    self.green_light.setStyleSheet("background-color: rgba(0,255,0,200);\n" "border:3px solid black;\n")
                else:
                    self.red_light.setStyleSheet("background-color: rgba(255,0,0,200);\n" "border:3px solid black;\n")
                    self.green_light.setStyleSheet("background-color: rgba(0,255,0,0);\n" "border:3px solid black;\n")
            else:
                self.green_light.setStyleSheet("background-color: rgba(0,255,0,0);\n" "border:3px solid black;\n")
                self.red_light.setStyleSheet("background-color: rgba(255,0,0,0);\n" "border:3px solid black;\n")











    def _handler(self):
        self.timer = QTimer()
        self.timer.setInterval(100)  # refreshes every time period
        self.timer.timeout.connect(self.update)
        self.timer.start()
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Track Model"))
        self.title.setText(_translate("MainWindow", "Track Map"))
        # self.clock.setText(_translate("MainWindow", "13:24:55"))

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
        self.t_station.setText(_translate("MainWindow", "Station Side"))
        self.t_station_name.setText(_translate("MainWindow", "Station Name"))
        self.t_pwr_fail.setText(_translate("MainWindow", "Power Failure"))
        self.t_circ_fail.setText(_translate("MainWindow", "Circuit Failure"))
        self.t_broke_rail.setText(_translate("MainWindow", "Broken Rail"))
        self.power_failure.setText(_translate("MainWindow", "Off"))
        self.broken_rail.setText(_translate("MainWindow", "Off"))
        self.circuit_failure.setText(_translate("MainWindow", "Off"))
        self.t_heater_fail.setText(_translate("MainWindow", "Track Heater Failure"))
        self.track_heater.setText(_translate("MainWindow", "Off"))
        self.t_temp_control.setText(_translate("MainWindow", "Track Heaters"))

    def browse_files(self):
        browse = QFileDialog.getOpenFileName(self.load_file)
        self._filepath = (browse[0])
        self.block_data = block_info(self._filepath)
        self.red_data = self.block_data.get_all_blocks_for_line('red')
        self.green_data = self.block_data.get_all_blocks_for_line('green')

#Error Detection
    def circuit_failure_clicked(self):
        if self.block_clicked == False:
            return
        tof = self.circuit_failure_detected
        if tof == False:
            self.circuit_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(0, 255, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
            self.circuit_failure.setText("ON")
        else:
            self.circuit_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
            self.circuit_failure.setText("OFF")
        self.circuit_failure_detected = not tof
        self.track_model.set_circuit_failure(self.circuit_failure_detected)

    def power_failure_clicked(self):
        if self.block_clicked == False:
            return
        tof = self.power_failure_detected
        if tof == False:
            self.power_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
                                               "background-color: rgb(0, 255, 0);\n"
                                               "border: 1px solid black;\n"
                                               "color: rgb(255, 255, 255)")
            self.power_failure.setText("ON")
        else:
            self.power_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
                                               "background-color: rgb(255, 0, 0);\n"
                                               "border: 1px solid black;\n"
                                               "color: rgb(255, 255, 255)")
            self.power_failure.setText("OFF")
        self.power_failure_detected = not tof
        self.track_model.set_power_failure(self.power_failure_detected)

    def broken_rail_clicked(self):
        if self.block_clicked == False:
            return
        tof = self.broken_rail_detected
        if tof == False:
            self.broken_rail.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
                                               "background-color: rgb(0, 255, 0);\n"
                                               "border: 1px solid black;\n"
                                               "color: rgb(255, 255, 255)")
            self.broken_rail.setText("ON")
        else:
            self.broken_rail.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
                                               "background-color: rgb(255, 0, 0);\n"
                                               "border: 1px solid black;\n"
                                               "color: rgb(255, 255, 255)")
            self.broken_rail.setText("OFF")
        self.broken_rail_detected = not tof
        self.track_model.set_broken_rail(self.broken_rail_detected)

    def heater_failure_clicked(self):
        if self.block_clicked == False:
            return

        tof = self.heater_failure_detected
        if tof == False:
            self.track_heater.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
                                           "background-color: rgb(0, 255, 0);\n"
                                           "border: 1px solid black;\n"
                                           "color: rgb(255, 255, 255)")
            self.track_heater.setText("ON")
        else:
            self.track_heater.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
                                           "background-color: rgb(255, 0, 0);\n"
                                           "border: 1px solid black;\n"
                                           "color: rgb(255, 255, 255)")
            self.track_heater.setText("OFF")
        self.heater_failure_detected = not tof
        self.track_model.set_heater_failure(self.heater_failure_detected)



    def update_map_occupancy(self, occupied_blocks):
        try:
            if self.line_picked == 'green':
                for button_id in occupied_blocks:
                    # print(button_id)
                    row = button_id // self.green_map.columnCount()
                    column = (button_id % self.green_map.columnCount())-1
                    item = QTableWidgetItem()
                    item.setBackground(QColor(0,255,0))
                    self.green_map.setItem(row, column, item)
                    if button_id != 1:
                        row2 = (button_id-1) // self.green_map.columnCount()
                        column2 = ((button_id-1) % self.green_map.columnCount())-1
                        item2 = QTableWidgetItem()
                        item2.setBackground(QColor(255,255,255))
                        self.green_map.setItem(row2,column2,item2)
            elif self.line_picked == 'red':
                for button_id in occupied_blocks:
                    row = button_id // self.red_map.columnCount()
                    column = (button_id % self.red_map.columnCount())-1
                    item = QTableWidgetItem()
                    item.setBackground(QColor(0,255,0))
                    self.red_map.setItem(row, column, item)
            else:
                pass
        except Exception as e:
            print(e)

    def up_temp(self):
        sign = random.choice([-1,1])
        self.environment_temp += sign * .001
        self.e_temp.setText(str(format(self.environment_temp,".1f")))

    def track_heater_control(self,value):
        self.heater_temp.setText(str(value))

    def clear_labels(self):
        self.station_name.setText("")
        self.block_length.setText("")
        self.speed_limit.setText("")
        self.switch_position.setText("")
        self.grade.setText("")
        self.elevation.setText("")
        self.underground.setText("")
        self.section.setText("")
        self.station.setText("")
        self.block_display.setText("")
        self.occupancy.setText("")
        self.green_light.setStyleSheet("background-color: rgba(0,255,0,0);\n" "border:3px solid black;\n")
        self.red_light.setStyleSheet("background-color: rgba(0,255,0,0);\n" "border:3px solid black;\n")
        self.direction.setText("")
        self.heater_temp.setText("")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    e = Ui_MainWindow(TrackModel(TrackControllerTrackModelAPI(), TrackModelTrainModelAPI()))

    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())
