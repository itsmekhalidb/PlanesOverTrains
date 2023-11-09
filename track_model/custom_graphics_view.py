from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsPathItem
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, QtWidgets
from track_model.block_info import block_info


class CustomGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()



    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), QtGui.QTransform())
        if isinstance(item, QGraphicsPathItem):
            block_id = item.data(0)
            if block_id:
                print(f"Clicked on {block_id}")

        super().mousePressEvent(event)







