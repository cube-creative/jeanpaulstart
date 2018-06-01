import os
import sys
import logging
from PySide.QtGui import *
from PySide.QtCore import *

from jeanpaulstartui import ROOT
from jeanpaulstartui.view.flow_layout import FlowLayout
from jeanpaulstartui.view.progress_label import ProgressLabel


def _clear_layout(layout):
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().deleteLater()


class LauncherWidget(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)

        self.mouse_pressed = False
        self.offset = QCursor()
        self.window_icon = QIcon(ROOT + '/resources/ceci-n-est-pas-une-icone.png')

        self.settings = QSettings('CubeCreative', 'JeanPaulStart')
        self.restoreGeometry(self.settings.value('geometry', ''))

        self.setMouseTracking(True)
        self.setObjectName('LauncherWidget')
        self.setWindowTitle('Jean-Paul Start')
        self.setWindowIcon(self.window_icon)
        self.setMinimumSize(376, 144)
        self.setWindowFlags(
            Qt.CustomizeWindowHint |
            Qt.Dialog |
            Qt.WindowCloseButtonHint |
            Qt.WindowMinimizeButtonHint |
            Qt.WindowSystemMenuHint
        )

        batches_widget = QWidget()
        self.batches_layout = FlowLayout(parent=batches_widget, spacing=0)
        batches_widget.setLayout(self.batches_layout)
        batches_widget.setContentsMargins(16, 16, 16, 16)
        self.batches_layout.setSpacing(16)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(batches_widget)
        self.scroll_area.setWidgetResizable(True)

        self.status_progress_bar = ProgressLabel()
        self.status_progress_bar.setFixedHeight(15)
        self.status_progress_bar.setObjectName("status")

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.status_progress_bar)
        self.main_layout.setContentsMargins(8, 8, 8, 8)

        self.controller = None

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.window_icon)
        self.tray.setToolTip('Jean-Paul Start')
        self.tray.setVisible(True)
        self.tray.activated.connect(self.showNormalReason)

        menu = QMenu()
        self.version_menu = menu.addAction('')
        self.version_menu.setDisabled(True)
        menu.addSeparator()
        open_action = menu.addAction("Open Jean-Paul Start")
        open_action.triggered.connect(self.showNormal)
        reload_action = menu.addAction("Reload batches")
        reload_action.triggered.connect(self.reload_batches)
        menu.addSeparator()
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(sys.exit)
        self.tray.setContextMenu(menu)

    def refresh(self):
        QApplication.processEvents()

    def set_hourglass(self, is_hourglass):
        if is_hourglass:
            QApplication.setOverrideCursor(Qt.WaitCursor)
        else:
            QApplication.restoreOverrideCursor()

    def set_status_message(self, message):
        self.status_progress_bar.setText(message)

    def set_progress(self, value):
        self.status_progress_bar.set_progress(value)

    def set_version(self, version):
        self.version_menu.setText(version)
        self.set_status_message(version)

    def show(self):
        self.tray.show()
        return QWidget.show(self)

    def showNormal(self):
        self.activateWindow()
        return QWidget.showNormal(self)

    def showNormalReason(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F5:
            self.reload_batches()
        QWidget.keyPressEvent(self, event)

    def reload_batches(self):
        self.showNormal()
        QApplication.setOverrideCursor(Qt.BusyCursor)
        self.controller.update()
        QApplication.restoreOverrideCursor()

    def populate_layout(self, batches):
        _clear_layout(self.batches_layout)
        for batch in batches:
            batch_button = self._make_batch_button(batch)
            self.batches_layout.addWidget(batch_button)

    def _make_batch_button(self, batch):
        button = QPushButton(self)
        button_icon = QLabel()

        image_path = os.path.expandvars(batch['icon_path'])
        if os.path.isfile(image_path):
            image = QImage(image_path)
        else:
            image = QImage(2, 2, QImage.Format_RGB16)
            logging.warn("Impossible to find " + image_path)
        button_icon.setPixmap(QPixmap.fromImage(image.scaled(
            48,
            48,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation
        )))

        button_icon.setAlignment(Qt.AlignCenter)
        button_icon.setTextInteractionFlags(Qt.NoTextInteraction)
        button_icon.setMouseTracking(False)
        button_icon.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_icon.setContentsMargins(0, 8, 0, 0)

        batch_name = batch['name']
        button_text = QLabel(batch_name)
        button_text.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        button_text.setWordWrap(True)
        button_text.setTextInteractionFlags(Qt.NoTextInteraction)
        button_text.setMouseTracking(False)
        button_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        button_layout = QVBoxLayout()
        button_layout.addWidget(button_icon)
        button_layout.addWidget(button_text)
        button_layout.setSpacing(0)
        button_layout.setContentsMargins(4, 4, 4, 4)

        button.setText('')
        button.setDefault(True)
        button.setFixedSize(96, 96)
        button.setObjectName(batch['name'] + '_button')
        button.setLayout(button_layout)
        button.setCursor(QCursor(Qt.PointingHandCursor))

        button.batch = batch
        button.clicked.connect(self._batch_clicked)

        return button

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())
        self.hide()
        event.ignore()

    def _batch_clicked(self):
        batch_button = self.sender()
        self.controller.batch_clicked(batch_button.batch)
