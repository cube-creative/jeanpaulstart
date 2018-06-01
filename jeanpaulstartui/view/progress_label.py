from PySide.QtGui import *
from PySide.QtCore import Qt


class ProgressLabel(QLabel):

    def __init__(self, parent=None):
        QLabel.__init__(self, parent=parent)
        self._progress = 0.0

    def set_progress(self, value):
        self._progress = value

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(61, 174, 233))
        painter.drawRect(event.rect().adjusted(0, 13, -self.width()*(1 - self._progress), 0))
        painter.end()

        QLabel.paintEvent(self, event)
