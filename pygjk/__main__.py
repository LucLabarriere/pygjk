import sys
from PyQt6 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
from pygjk.tools import *


@dataclass
class Window(QtWidgets.QMainWindow):
    _request_go_up = False
    _request_go_down = False
    _request_go_left = False
    _request_go_right = False

    _request_rotate_right = False
    _request_rotate_left = False

    _request_scale_up = False
    _request_scale_down = False

    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Z:
            self._request_go_up = True
        if event.key() == QtCore.Qt.Key.Key_S:
            self._request_go_down = True
        if event.key() == QtCore.Qt.Key.Key_Q:
            self._request_go_left = True
        if event.key() == QtCore.Qt.Key.Key_D:
            self._request_go_right = True

        if event.key() == QtCore.Qt.Key.Key_E:
            self._request_rotate_right = True
        if event.key() == QtCore.Qt.Key.Key_A:
            self._request_rotate_left = True

        if event.key() == QtCore.Qt.Key.Key_C:
            self._request_scale_up = True
        if event.key() == QtCore.Qt.Key.Key_X:
            self._request_scale_down = True

    def keyReleaseEvent(self, event):
        if event.key() == QtCore.Qt.Key.Key_Z:
            self._request_go_up = False
        if event.key() == QtCore.Qt.Key.Key_S:
            self._request_go_down = False
        if event.key() == QtCore.Qt.Key.Key_Q:
            self._request_go_left = False
        if event.key() == QtCore.Qt.Key.Key_D:
            self._request_go_right = False

        if event.key() == QtCore.Qt.Key.Key_E:
            self._request_rotate_right = False
        if event.key() == QtCore.Qt.Key.Key_A:
            self._request_rotate_left = False

        if event.key() == QtCore.Qt.Key.Key_C:
            self._request_scale_up = False
        if event.key() == QtCore.Qt.Key.Key_X:
            self._request_scale_down = False


class Application(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([''])

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(QtWidgets.QVBoxLayout())

        self.canvas = pg.GraphicsLayoutWidget()
        self.main_widget.layout().addWidget(self.canvas)

        self.view = self.canvas.addViewBox()
        self.view.setAspectLocked(True)
        self.view.setRange(QtCore.QRectF(-2.5, -2.5, 5, 5))

        self._window = Window()
        self._window.setCentralWidget(self.main_widget)

        self._window.show()

        self.scatter = pg.ScatterPlotItem(size=10)
        self.view.addItem(self.scatter)

        self.main_shape = Shape()
        self.translation_speed = 0.003 
        self.rotation_speed = 0.1
        self.scale_speed = 0.001 

        # Original shape is red
        self.main_shape.setColor([255, 0, 0, 255])
        self.scatter.addPoints(self.main_shape.getFormattedPoints())

        self.update_clock = QtCore.QTimer()
        self.dt = 15 
        self.update_clock.setInterval(self.dt)
        self.update_clock.timeout.connect(self.update)
        self.update_clock.start()

        sys.exit(self.exec())

    def update(self):
        if self._window._request_go_up:
            self.main_shape.transform.translate([0.0, self.dt * self.translation_speed, 0.0])
        if self._window._request_go_down:
            self.main_shape.transform.translate([0.0, - self.dt * self.translation_speed, 0.0])
        if self._window._request_go_left:
            self.main_shape.transform.translate([- self.dt * self.translation_speed, 0.0, 0.0])
        if self._window._request_go_right:
            self.main_shape.transform.translate([self.dt * self.translation_speed, 0.0, 0.0])

        if self._window._request_rotate_left:
            self.main_shape.transform.rotate([0.0, 0.0, self.dt * self.rotation_speed])
        if self._window._request_rotate_right:
            self.main_shape.transform.rotate([0.0, 0.0, -self.dt * self.rotation_speed])

        if self._window._request_scale_up:
            self.main_shape.transform.scale([self.dt * self.scale_speed, self.dt * self.scale_speed, 0.0])
        if self._window._request_scale_down:
            self.main_shape.transform.scale([- self.dt * self.scale_speed, - self.dt * self.scale_speed, 0.0])

        self.scatter.setData(self.main_shape.getFormattedPoints())


if __name__ == '__main__':
    app = Application()
