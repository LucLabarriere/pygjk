import sys, os
from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from pygjk.rendering import Renderer
from pygjk.tools import *
from pygjk import physics
from pygjk.algo import Algo


class Window(QtWidgets.QMainWindow):
    _key_UP = QtCore.Qt.Key.Key_W
    _key_LEFT = QtCore.Qt.Key.Key_A
    _key_DOWN = QtCore.Qt.Key.Key_S
    _key_RIGHT = QtCore.Qt.Key.Key_D
    _key_SCALE_UP = QtCore.Qt.Key.Key_C
    _key_SCALE_DOWN = QtCore.Qt.Key.Key_X
    _key_ROTATE_LEFT= QtCore.Qt.Key.Key_E
    _key_ROTATE_RIGHT = QtCore.Qt.Key.Key_Q

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

        if QtCore.QLocale().name() == 'fr_FR':
            Window._key_UP = QtCore.Qt.Key.Key_Z
            Window._key_LEFT = QtCore.Qt.Key.Key_Q
            Window._key_ROTATE_RIGHT = QtCore.Qt.Key.Key_A

    def keyPressEvent(self, event):
        if event.key() == Window._key_UP:
            self._request_go_up = True
        if event.key() == Window._key_DOWN: 
            self._request_go_down = True
        if event.key() == Window._key_LEFT:
            self._request_go_left = True
        if event.key() == Window._key_RIGHT:
            self._request_go_right = True

        if event.key() == Window._key_ROTATE_RIGHT:
            self._request_rotate_right = True
        if event.key() == Window._key_ROTATE_LEFT:
            self._request_rotate_left = True

        if event.key() == Window._key_SCALE_UP: 
            self._request_scale_up = True
        if event.key() == Window._key_SCALE_DOWN:
            self._request_scale_down = True

    def keyReleaseEvent(self, event):
        if event.key() == Window._key_UP:
            self._request_go_up = False
        if event.key() == Window._key_DOWN: 
            self._request_go_down = False
        if event.key() == Window._key_LEFT:
            self._request_go_left = False
        if event.key() == Window._key_RIGHT:
            self._request_go_right = False

        if event.key() == Window._key_ROTATE_RIGHT:
            self._request_rotate_right = False
        if event.key() == Window._key_ROTATE_LEFT:
            self._request_rotate_left = False

        if event.key() == Window._key_SCALE_UP: 
            self._request_scale_up = False
        if event.key() == Window._key_SCALE_DOWN:
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

        self._window = Window()
        self._window.setCentralWidget(self.main_widget)

        self._window.show()
        self._renderer = Renderer(self.view)

        self.view.setXRange(-2, 5, padding=0)
        self.view.setYRange(-2, 5, padding=0)

        self.translation_speed = 0.006
        self.rotation_speed = 0.5
        self.scale_speed = 0.01

        # API Usage :
        # Creating Shape object which contains a transform and primitive points
        self.main_shape_id, _ = self._renderer.create_shape()

        # Setting the color of a shape for pyqtgraph rendering
        self._renderer.get_shape(self.main_shape_id).set_color([255, 255, 255, 255])

        # Creating random shapes
        for _ in range(30):
            self._renderer.create_random_shape()

        self.update_clock = QtCore.QTimer()
        self.dt = 17
        self.update_clock.setInterval(self.dt)
        self.update_clock.timeout.connect(self.update)
        self.update_clock.start()

        sys.exit(self.exec())

    def update(self):
        self._renderer.reset_colors()
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
            main_shape.transform.increment_scale([self.dt * self.scale_speed, self.dt * self.scale_speed, 0.0])
        if self._window._request_scale_down:
            main_shape.transform.increment_scale([- self.dt * self.scale_speed, - self.dt * self.scale_speed, 0.0])

        main_shape.set_dirty()
        physics.Engine.update(self.dt, self._renderer.shapes)
        self._renderer.render()
        self._renderer.render_update_time(physics.Engine.get_update_time())

