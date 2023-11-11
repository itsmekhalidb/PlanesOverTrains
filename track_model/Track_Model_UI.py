from PyQt5 import QtCore, QtGui, QtWidgets
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsPathItem
from PyQt5.QtGui import QPen, QBrush, QColor, QTransform
from PyQt5.QtCore import Qt
from api.track_model_train_model_api import TrackModelTrainModelAPI
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
        self.setupUi()
        self.show()

        self._filepath = ""

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1143, 938)
        self.trackmodel_main = QtWidgets.QWidget(self)
        self.trackmodel_main.setObjectName("trackmodel_main")

        scene = CustomGraphicsScene()
        #scene = QGraphicsScene(self.trackmodel_main)
        scene.setSceneRect(0, 61, 1142, 600)


        red_pen = QPen(Qt.red)
        red_pen.setWidth(5)
        red_pen_2 = QPen(QColor(200,0,0))
        red_pen_2.setWidth(5)

        path_data = [
            {
                'start': QPointF(725, 220),
                'points': [QPointF(725, 220), QPointF(760, 205)],       #A
                'label': "1"
            },
            {
                'start': QPointF(760, 205),
                'points': [QPointF(760, 205), QPointF(790, 185)],
                'label': "2"
            },
            {
                'start': QPointF(790, 185),
                'points': [QPointF(790,185), QPointF(820, 165)],
                'label': "3"
            },
            {
                'start': QPointF(820, 165),
                'points': [QPointF(820,165), QPointF(840,145)],         #B
                'label': "4"
            },
            {
                'start': QPointF(840,145),
                'points': [QPointF(840,145), QPointF(860, 125)],
                'label': "5"
            },
            {
                'start': QPointF(860, 125),
                'points': [QPointF(860,125), QPointF(890,115)],
                'label': "6"
            },
            {
                'start': QPointF(890,115),
                'points': [QPointF(890,115), QPointF(920,120)],         #C
                'label': "7"
            },
            {
                'start': QPointF(920,120),
                'points': [QPointF(920,120), QPointF(950,125)],
                'label': "8"
            },
            {
                'start': QPointF(950,125),
                'points': [QPointF(950,125), QPointF(980,145)],
                'label': "9"
            },
            {
                'start': QPointF(980,145), #38, 18, 855, 220            #D
                'points': [QPointF(980,145),QPointF(935,175)],
                'label': "10"
            },
            {
                'start': QPointF(935,175),
                'points': [QPointF(935,175), QPointF(885, 200)],
                'label': "11"
            },
            {
                'start': QPointF(885,200),
                'points': [QPointF(885,200), QPointF(840, 220)],
                'label': "12"
            },
            {#725,220
                'start': QPointF(840,220),                              #E
                'points': [QPointF(840,220),QPointF(805,220)],
                'label': "13"
            },
            {
                'start': QPointF(805,220),
                'points': [QPointF(805,220),QPointF(765,220)],
                'label': "14"
            },
            {
                'start': QPointF(765,220),
                'points': [QPointF(765,220), QPointF(725,220)],
                'label': "15"
            },
            {
                'start': QPointF(725,220),                              #F
                'points': [QPointF(725,220), QPointF(700,220)],
                'label': "16"
            },
            {
                'start': QPointF(700,220),
                'points': [QPointF(700,220), QPointF(680,220)],
                'label': "17"
            },
            {
                'start': QPointF(680,220),
                'points': [QPointF(680,220), QPointF(660,220)],
                'label': "18"
            },
            {
                'start': QPointF(660,220),
                'points': [QPointF(660,220), QPointF(640,220)],
                'label': "19"
            },
            {
                'start': QPointF(640,220),
                'points': [QPointF(640,220), QPointF(620,220)],
                'label': "20"
            },
            {
                'start': QPointF(620,220),                              #G
                'points': [QPointF(620,220), QPointF(595,225)],
                'label': "21"
            },
            {
                'start': QPointF(595,225),
                'points': [QPointF(595,225), QPointF(570,235)],
                'label': "22"
            },
            {
                'start': QPointF(570,235),
                'points': [QPointF(570,235), QPointF(545, 250)],
                'label': "23"
            },
            {
                'start': QPointF(545,250),                              #H
                'points': [QPointF(545,250), QPointF(545,262)],
                'label': "24"
            },
            {
                'start': QPointF(545,262),
                'points': [QPointF(545,262), QPointF(545,274)],
                'label': "25"
            },
            {
                'start': QPointF(545,274),
                'points': [QPointF(545,274), QPointF(545,286)],
                'label': "26"
            },
            {
                'start': QPointF(545,286),
                'points': [QPointF(545,286),QPointF(545,298)],
                'label': "27"
            },
            {
                'start': QPointF(545,298),
                'points': [QPointF(545,298),QPointF(545,310)],
                'label': "28"
            },
            {
                'start': QPointF(545,310),
                'points': [QPointF(545,310), QPointF(545,322)],
                'label': "29"
            },
            {
                'start': QPointF(545,322),
                'points': [QPointF(545,322), QPointF(545,334)],
                'label': "30"
            },
            {
                'start': QPointF(545,334),
                'points': [QPointF(545,334), QPointF(545, 346)],
                'label': "31"
            },
            {
                'start': QPointF(545,346),
                'points': [QPointF(545,346), QPointF(545,358)],
                'label': "32"
            },
            {
                'start': QPointF(545,358),
                'points': [QPointF(545,358), QPointF(545, 370)],
                'label': "33"
            },
            {
                'start': QPointF(545,370),
                'points': [QPointF(545,370), QPointF(545, 382)],
                'label': "34"
            },
            {
                'start': QPointF(545,382),
                'points': [QPointF(545, 382), QPointF(545, 394)],
                'label': "35"
            },
            {
                'start': QPointF(545,394),
                'points': [QPointF(545,394), QPointF(545,406)],
                'label': "36"
            },
            {
                'start': QPointF(545,406),
                'points': [QPointF(545,406), QPointF(545, 418)],
                'label': "37"
            },
            {
                'start': QPointF(545,418),
                'points': [QPointF(545,418), QPointF(545, 430)],
                'label': "38"
            },
            {
                'start': QPointF(545,430),
                'points': [QPointF(545,430), QPointF(545, 442)],
                'label': "39"
            },
            {
                'start': QPointF(545, 442),
                'points': [QPointF(545, 442), QPointF(545, 454)],
                'label': "40"
            },
            {
                'start': QPointF(545,454),
                'points': [QPointF(545,454), QPointF(545, 466)],
                'label': "41"
            },
            {
                'start': QPointF(545, 466),
                'points': [QPointF(545,466), QPointF(545, 478)],
                'label': "42"
            },
            {
                'start': QPointF(545,478),
                'points': [QPointF(545,478), QPointF(545, 490)],
                'label': "43"
            },
            {
                'start': QPointF(545,490),
                'points': [QPointF(545,490), QPointF(545, 502)],
                'label': "44"
            },
            {
                'start': QPointF(545,502),
                'points': [QPointF(545,502), QPointF(545,514)],
                'label': "45"
            },
            {
                'start': QPointF(545,514),                              #I
                'points': [QPointF(545,514), QPointF(520, 545)],
                'label': "46"
            },
            {
                'start': QPointF(520,545),
                'points': [QPointF(520,545), QPointF(500,565)],
                'label': "47"
            },
            {
                'start': QPointF(500,565),
                'points': [QPointF(500,565), QPointF(465,575)],
                'label': "48"
            },
            {
                'start': QPointF(465,575),                              #J
                'points': [QPointF(465,575), QPointF(440, 575)],
                'label': "49"
            },
            {
                'start': QPointF(440,575),
                'points': [QPointF(440,575), QPointF(415,575)],
                'label': "50"
            },
            {
                'start': QPointF(415, 575),
                'points': [QPointF(415,575), QPointF(390,575)],
                'label': "51"
            },
            {
                'start': QPointF(390,575),
                'points': [QPointF(390,575), QPointF(365,575)],
                'label': "52"
            },
            {
                'start': QPointF(365,575),
                'points': [QPointF(365,575), QPointF(340,575)],
                'label': "53"
            },
            {
                'start': QPointF(340,575),
                'points': [QPointF(340,575), QPointF(315,575)],
                'label': "54"
            },
            {
                'start': QPointF(315,575),                                 #K
                'points': [QPointF(315,575), QPointF(290, 550)],
                'label': "55"
            },
            {
                'start': QPointF(290,550),
                'points': [QPointF(290,550), QPointF(265, 520)],
                'label': "56"
            },
            {
                'start': QPointF(265,520),
                'points': [QPointF(265,520), QPointF(240, 485)],
                'label': "57"
            },
            {
                'start': QPointF(240,485),                                  #L
                'points': [QPointF(240,485), QPointF(250, 455)],
                'label': "58"
            },
            {
                'start': QPointF(250,455),
                'points': [QPointF(250,455), QPointF(270,435)],
                'label': "59"
            },
            {
                'start': QPointF(270,435),
                'points': [QPointF(270,435), QPointF(290,420)],
                'label': "60"
            },
            {
                'start': QPointF(290,420),                                  #M
                'points': [QPointF(290,420), QPointF(320, 460)],
                'label': "61"
            },
            {
                'start': QPointF(320,460),
                'points': [QPointF(320,460), QPointF(335,510)],
                'label': "62"
            },
            {
                'start': QPointF(335,510),
                'points': [QPointF(335,510), QPointF(345,535)],
                'label': "63"
            },
            {#x = 415 | y = 575
                'start': QPointF(345,535),                                  #N
                'points': [QPointF(345,535), QPointF(365,550)],
                'label': "64"
            },
            {
                'start': QPointF(365,550),
                'points': [QPointF(365,550), QPointF(390, 565)],
                'label': "65"
            },
            {
                'start': QPointF(390,565),
                'points': [QPointF(390,565), QPointF(415, 575)],
                'label': "66"
            },
            {
                'start': QPointF(542,490),                                  #O
                'points': [QPointF(542,490), QPointF(507,470)],
                'label': "67"
            },
            {
                'start': QPointF(507,470),                                  #P
                'points': [QPointF(507,470), QPointF(507,455)],
                'label': "68"
            },
            {
                'start': QPointF(507,455),
                'points': [QPointF(507,455), QPointF(507, 440)],
                'label': "69"
            },
            {
                'start': QPointF(507,440),
                'points': [QPointF(507,440), QPointF(507,425)],
                'label': "70"
            },
            {
                'start': QPointF(507,425),                                  #Q
                'points': [QPointF(507,425), QPointF(542,405)],
                'label': "71"
            },
            {
                'start': QPointF(542,345),                                  #R
                'points': [QPointF(542,345),QPointF(507,335)],
                'label': "72"
            },
            {
                'start': QPointF(507,335),                                  #S
                'points': [QPointF(507,335), QPointF(507,310)],
                'label': "73"
            },
            {
                'start': QPointF(507,310),
                'points': [QPointF(507,310), QPointF(507,295)],
                'label': "74"
            },
            {
                'start': QPointF(507,295),
                'points': [QPointF(507,295), QPointF(507,280)],
                'label': "75"
            },
            {
                'start': QPointF(507,280),                                  #T
                'points': [QPointF(507,280), QPointF(542,260)],
                'label': "76"
            }

        ]



        for i, data in enumerate(path_data):
            path = QPainterPath()
            path.moveTo(data['start'])
            for point in data['points']:
                path.quadTo(point, point)

            r = QGraphicsPathItem(path)
            r.setData(0, data['label'])
            r.setPen(red_pen)
            if i%2 == 0:
                r.setPen(red_pen)
            else:
                r.setPen(red_pen_2)

            scene.addItem(r)

        red_pen = QPen(Qt.red)
        red_pen.setWidth(4)
        red_2 = QPen(Qt.darkRed)
        red_2.setWidth(4)





        self.graph_view = QtWidgets.QGraphicsView(scene, self.trackmodel_main)
        self.graph_view.setGeometry(QtCore.QRect(0, 61, 1142, 600))

        self.load_file = QtWidgets.QPushButton(self.trackmodel_main, clicked=lambda: self.browse_files())
        self.load_file.setGeometry(QtCore.QRect(600,10,60,41))
        self.load_file.setText("Load File")
        self.load_file.setStyleSheet("background-color: rgb(255,255,255);\n""border: 2px solid black;\n""font: 87 8pt \"Arial\";")

        self.block_display = QtWidgets.QLabel(self.trackmodel_main)
        self.block_display.setGeometry(QtCore.QRect(155,10,60,41))
        self.block_display.setText("")
        self.block_display.setStyleSheet("background-color: rgb(255,255,255);\n""border: 2px solid black;\n""font: 87 10pt \"Arial Black\";")

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
        self.static_title.setGeometry(QtCore.QRect(0, 660, 461, 41))
        self.static_title.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"background-color: rgb(134, 177, 255);\n"
"border: 2px solid black;")
        self.static_title.setAlignment(QtCore.Qt.AlignCenter)
        self.static_title.setObjectName("static_title")
        self.t_spd_limit = QtWidgets.QLabel(self.trackmodel_main)
        self.t_spd_limit.setGeometry(QtCore.QRect(0, 700, 141, 41))
        self.t_spd_limit.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_spd_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.t_spd_limit.setObjectName("t_spd_limit")
        self.t_block_length = QtWidgets.QLabel(self.trackmodel_main)
        self.t_block_length.setGeometry(QtCore.QRect(0, 750, 141, 41))
        self.t_block_length.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_block_length.setAlignment(QtCore.Qt.AlignCenter)
        self.t_block_length.setObjectName("t_block_length")
        self.t_grade = QtWidgets.QLabel(self.trackmodel_main)
        self.t_grade.setGeometry(QtCore.QRect(0, 800, 141, 41))
        self.t_grade.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_grade.setAlignment(QtCore.Qt.AlignCenter)
        self.t_grade.setObjectName("t_grade")
        self.t_elevation = QtWidgets.QLabel(self.trackmodel_main)
        self.t_elevation.setGeometry(QtCore.QRect(0, 850, 141, 41))
        self.t_elevation.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_elevation.setAlignment(QtCore.Qt.AlignCenter)
        self.t_elevation.setObjectName("t_elevation")
        self.speed_limit = QtWidgets.QLabel(self.trackmodel_main)
        self.speed_limit.setGeometry(QtCore.QRect(140, 700, 71, 41))
        self.speed_limit.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.speed_limit.setText("")
        self.speed_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.speed_limit.setObjectName("speed_limit")
        self.block_length = QtWidgets.QLabel(self.trackmodel_main)
        self.block_length.setGeometry(QtCore.QRect(140, 750, 71, 41))
        self.block_length.setStyleSheet("font: 87 9pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.block_length.setText("")
        self.block_length.setAlignment(QtCore.Qt.AlignCenter)
        self.block_length.setObjectName("block_length")
        self.grade = QtWidgets.QLabel(self.trackmodel_main)
        self.grade.setGeometry(QtCore.QRect(140, 800, 71, 41))
        self.grade.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.grade.setText("")
        self.grade.setAlignment(QtCore.Qt.AlignCenter)
        self.grade.setObjectName("grade")
        self.elevation = QtWidgets.QLabel(self.trackmodel_main)
        self.elevation.setGeometry(QtCore.QRect(140, 850, 71, 41))
        self.elevation.setStyleSheet("font: 87 9pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.elevation.setText("")
        self.elevation.setAlignment(QtCore.Qt.AlignCenter)
        self.elevation.setObjectName("elevation")
        self.t_section = QtWidgets.QLabel(self.trackmodel_main)
        self.t_section.setGeometry(QtCore.QRect(250, 700, 141, 41))
        self.t_section.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_section.setAlignment(QtCore.Qt.AlignCenter)
        self.t_section.setObjectName("t_section")
        self.section = QtWidgets.QLabel(self.trackmodel_main)
        self.section.setGeometry(QtCore.QRect(390, 700, 71, 41))
        self.section.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.section.setText("")
        self.section.setAlignment(QtCore.Qt.AlignCenter)
        self.section.setObjectName("section")
        self.t_swtch_pos = QtWidgets.QLabel(self.trackmodel_main)
        self.t_swtch_pos.setGeometry(QtCore.QRect(250, 750, 141, 41))
        self.t_swtch_pos.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_swtch_pos.setAlignment(QtCore.Qt.AlignCenter)
        self.t_swtch_pos.setObjectName("t_swtch_pos")
        self.t_occupied = QtWidgets.QLabel(self.trackmodel_main)
        self.t_occupied.setGeometry(QtCore.QRect(250, 800, 141, 41))
        self.t_occupied.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_occupied.setAlignment(QtCore.Qt.AlignCenter)
        self.t_occupied.setObjectName("t_occupied")
        self.t_undr = QtWidgets.QLabel(self.trackmodel_main)
        self.t_undr.setGeometry(QtCore.QRect(250, 850, 141, 41))
        self.t_undr.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_undr.setAlignment(QtCore.Qt.AlignCenter)
        self.t_undr.setObjectName("t_undr")
        self.switch_position = QtWidgets.QLabel(self.trackmodel_main)
        self.switch_position.setGeometry(QtCore.QRect(390, 750, 71, 41))
        self.switch_position.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.switch_position.setText("")
        self.switch_position.setAlignment(QtCore.Qt.AlignCenter)
        self.switch_position.setObjectName("switch_position")
        self.occupancy = QtWidgets.QLabel(self.trackmodel_main)
        self.occupancy.setGeometry(QtCore.QRect(390, 800, 71, 41))
        self.occupancy.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.occupancy.setText("")
        self.occupancy.setAlignment(QtCore.Qt.AlignCenter)
        self.occupancy.setObjectName("occupancy")
        self.underground = QtWidgets.QLabel(self.trackmodel_main)
        self.underground.setGeometry(QtCore.QRect(390, 850, 71, 41))
        self.underground.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.underground.setText("")
        self.underground.setAlignment(QtCore.Qt.AlignCenter)
        self.underground.setObjectName("underground")
        self.static_title_2 = QtWidgets.QLabel(self.trackmodel_main)
        self.static_title_2.setGeometry(QtCore.QRect(460, 660, 241, 41))
        self.static_title_2.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"background-color: rgb(134, 177, 255);\n"
"border: 2px solid black;")
        self.static_title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.static_title_2.setObjectName("static_title_2")
        self.static_title_3 = QtWidgets.QLabel(self.trackmodel_main)
        self.static_title_3.setGeometry(QtCore.QRect(700, 660, 441, 41))
        self.static_title_3.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"background-color: rgb(134, 177, 255);\n"
"border: 2px solid black;")
        self.static_title_3.setAlignment(QtCore.Qt.AlignCenter)
        self.static_title_3.setObjectName("static_title_3")
        self.line = QtWidgets.QFrame(self.trackmodel_main)
        self.line.setGeometry(QtCore.QRect(450, 700, 20, 191))
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
        self.line_2.setGeometry(QtCore.QRect(690, 700, 20, 191))
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
        self.t_station.setGeometry(QtCore.QRect(460, 700, 151, 41))
        self.t_station.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_station.setAlignment(QtCore.Qt.AlignCenter)
        self.t_station.setObjectName("t_station")
        self.station = QtWidgets.QLabel(self.trackmodel_main)
        self.station.setGeometry(QtCore.QRect(610, 700, 81, 41))
        self.station.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 1px solid black;")
        self.station.setText("")
        self.station.setAlignment(QtCore.Qt.AlignCenter)
        self.station.setObjectName("station")
        self.t_station_name = QtWidgets.QLabel(self.trackmodel_main)
        self.t_station_name.setGeometry(QtCore.QRect(460, 750, 241, 41))
        self.t_station_name.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_station_name.setAlignment(QtCore.Qt.AlignCenter)
        self.t_station_name.setObjectName("t_station_name")
        self.station_name = QtWidgets.QLabel(self.trackmodel_main)
        self.station_name.setGeometry(QtCore.QRect(460, 790, 241, 101))
        self.station_name.setStyleSheet("font: 87 11pt \"Arial Black\";\n"
"background-color: rgb(255, 255, 255);\n"
"border: 2px solid black;")
        self.station_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.station_name.setText("")
        self.station_name.setAlignment(QtCore.Qt.AlignCenter)
        self.station_name.setObjectName("station_name")
        self.t_pwr_fail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_pwr_fail.setGeometry(QtCore.QRect(700, 700, 161, 41))
        self.t_pwr_fail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_pwr_fail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_pwr_fail.setObjectName("t_pwr_fail")
        self.t_circ_fail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_circ_fail.setGeometry(QtCore.QRect(700, 770, 161, 41))
        self.t_circ_fail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_circ_fail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_circ_fail.setObjectName("t_circ_fail")
        self.t_broke_rail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_broke_rail.setGeometry(QtCore.QRect(940, 770, 161, 41))
        self.t_broke_rail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_broke_rail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_broke_rail.setObjectName("t_broke_rail")
        self.power_failure = QtWidgets.QPushButton(self.trackmodel_main)
        self.power_failure.setGeometry(QtCore.QRect(860, 700, 41, 41))
        self.power_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.power_failure.setObjectName("power_failure")
        self.broken_rail = QtWidgets.QPushButton(self.trackmodel_main)
        self.broken_rail.setGeometry(QtCore.QRect(1100, 770, 41, 41))
        self.broken_rail.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.broken_rail.setObjectName("broken_rail")
        self.circuit_failure = QtWidgets.QPushButton(self.trackmodel_main)
        self.circuit_failure.setGeometry(QtCore.QRect(860, 770, 41, 41))
        self.circuit_failure.setStyleSheet("font: 87 10pt \"Arial Black\";\n"
"background-color: rgb(255, 0, 0);\n"
"border: 1px solid black;\n"
"color: rgb(255, 255, 255)")
        self.circuit_failure.setObjectName("circuit_failure")
        self.t_heater_fail = QtWidgets.QLabel(self.trackmodel_main)
        self.t_heater_fail.setGeometry(QtCore.QRect(940, 700, 161, 41))
        self.t_heater_fail.setStyleSheet("background-color: rgb(194, 194, 194);\n"
"font: 87 10pt \"Arial Black\";\n"
"border: 1px solid black;")
        self.t_heater_fail.setAlignment(QtCore.Qt.AlignCenter)
        self.t_heater_fail.setObjectName("t_heater_fail")
        self.track_heater = QtWidgets.QPushButton(self.trackmodel_main)
        self.track_heater.setGeometry(QtCore.QRect(1100, 700, 41, 41))
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

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self._handler()

    def update(self):
        _translate = QtCore.QCoreApplication.translate

        #self.clock.setText(self.track_model.get_time())
        self.track_model.set_filepath(self._filepath)

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





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    e = Ui_MainWindow(TrackModel(TrackControllerTrackModelAPI(), TrackModelTrainModelAPI()))
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())
