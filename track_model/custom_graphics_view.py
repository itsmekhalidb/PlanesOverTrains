from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt

class CustomGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            pos = event.pos()

            if 800 <= pos.x() <= 835 and 205 <= pos.y() <= 220:
                self.block_length.setText("50")
