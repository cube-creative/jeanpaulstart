from PySide.QtCore import *
from PySide.QtGui import *


"""
Flow Layout from
https://github.com/PySide/Examples/blob/master/examples/layouts/flowlayout.py
"""


class FlowLayout(QLayout):

    def __init__(self, parent=None, margin=0, spacing=-1):
        QLayout.__init__(self, parent)
        self.item_list = []

        if parent is None:
            self.setMargin(margin)
            self.setSpacing(spacing)

    def __del__(self):
        item = self.takeAt(0)
        while item:
            item = self.takeAt(0)

    def addItem(self, item):
        self.item_list.append(item)

    def count(self):
        return len(self.item_list)

    def itemAt(self, index):
        if index >= 0 and index < len(self.item_list):
            return self.item_list[index]
        return None

    def takeAt(self, index):
        if index >= 0 and index < len(self.item_list):
            return self.item_list.pop(index)

        return None

    def expandingDirections(self):
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        height = self.do_layout(QRect(0, 0, width, 0))
        return height

    def setGeometry(self, rect):
        super(FlowLayout, self).setGeometry(rect)
        self.do_layout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        # size = QSize()

        # for item in self.item_list:
        #    size = size.expandedTo(item.minimumSize())
        # size = size + QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        size = QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def do_layout(self, rect, test_only=True):
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self.item_list:
            widget = item.widget()
            space_x = self.spacing() + widget.style().layoutSpacing(QSizePolicy.PushButton,
                                                                    QSizePolicy.PushButton, Qt.Horizontal)
            space_y = self.spacing() + widget.style().layoutSpacing(QSizePolicy.PushButton,
                                                                    QSizePolicy.PushButton, Qt.Vertical) + 1
            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = next_x

            line_height = max(line_height, item.sizeHint().height())

        return y + line_height - rect.y()
