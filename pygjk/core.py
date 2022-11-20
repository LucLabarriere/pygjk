import sys
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from pygjk.rendering import Renderer
from pygjk.tools import *
from pygjk import physics
from pygjk.algo import Algo


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._request_go_up = False
        self._request_go_down = False
        self._request_go_left = False
        self._request_go_right = False
        self._request_rotate_right = False
        self._request_rotate_left = False
        self._request_scale_up = False
        self._request_scale_down = False

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
        Algo.initialize(self.view)

        self._window = Window()
        self._window.setCentralWidget(self.main_widget)

        self._window.show()
        self._renderer = Renderer(self.view)

        self.view.setXRange(0, 5, padding=0)
        self.view.setYRange(0, 5, padding=0)

        self.translation_speed = 0.003
        self.rotation_speed = 0.1
        self.scale_speed = 0.001

        # API Usage :
        # Creating Shape object which contains a transform and primitive points
        self.main_shape_id, _ = self._renderer.create_shape()

        # Setting the color of a shape for pyqtgraph rendering
        self._renderer.get_shape(self.main_shape_id).setColor([255, 255, 255, 255])

        # Creating random shapes
        for _ in range(5):
            self._renderer.create_random_shape()

        self.update_clock = QtCore.QTimer()
        self.dt = 15 
        self.update_clock.setInterval(self.dt)
        self.update_clock.timeout.connect(self.update)
        self.update_clock.start()

        sys.exit(self.exec())

    def update(self):
        main_shape = self._renderer.get_shape(self.main_shape_id)

        if self._window._request_go_up:
            main_shape.transform.translate(
                [0.0, self.dt * self.translation_speed, 0.0])
        if self._window._request_go_down:
            main_shape.transform.translate(
                [0.0, - self.dt * self.translation_speed, 0.0])
        if self._window._request_go_left:
            main_shape.transform.translate(
                [- self.dt * self.translation_speed, 0.0, 0.0])
        if self._window._request_go_right:
            main_shape.transform.translate(
                [self.dt * self.translation_speed, 0.0, 0.0])

        if self._window._request_rotate_left:
            main_shape.transform.rotate(
                [0.0, 0.0, self.dt * self.rotation_speed])
        if self._window._request_rotate_right:
            main_shape.transform.rotate(
                [0.0, 0.0, -self.dt * self.rotation_speed])

        if self._window._request_scale_up:
            main_shape.transform.scale(
                [self.dt * self.scale_speed, self.dt * self.scale_speed, 0.0])
        if self._window._request_scale_down:
            main_shape.transform.scale(
                [- self.dt * self.scale_speed, - self.dt * self.scale_speed, 0.0])

        self._renderer.render()
        physics.Engine.update(self.dt, self._renderer.shapes)

