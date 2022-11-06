from pygjk import shapes
from PyQt6 import QtWidgets
import numpy as np
import matplotlib.pyplot as plt
import copy
import sys


def get_direction(A: shapes.Shape, B: shapes.Shape) -> np.ndarray:
    return np.array(
        (B.center - A.center) / np.linalg.norm(B.center - A.center)
    )


class Application(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([''])

        points_a = np.array([
            [-0.5, -0.5, 0.0],
            [0.5, -0.5, 0.0],
            [-0.5, 0.5, 0.0],
            [0.5, 0.5, 0.0]
        ])

        points_b = copy.copy(points_a + np.array([-0.8, 0.7, 0.0]))
        points_c = copy.copy(points_a + np.array([2.0, -0.1, 0.0]))

        A = shapes.Shape(points_a, color='blue')
        B = shapes.Shape(points_b, color='orange')
        C = shapes.Shape(points_c, color='green')

        collection = [A, B, C]

        A.check_collision(B)

        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_subplot()
        ax.set_xlim(-3, 3)
        ax.set_ylim(-3, 3)

        for shape in collection:
            shape.draw(ax)

        direction_BC = get_direction(B, C)
        direction_CB = get_direction(C, B)

        B._support_function(direction_BC)
        B.draw_direction(direction_BC, ax)
        B.draw_support_point(direction_BC, ax)

        C._support_function(direction_CB)
        C.draw_direction(direction_CB, ax)
        C.draw_support_point(direction_CB, ax)

        self._window = QtWidgets.QMainWindow()
        self._window.setCentralWidget(fig.canvas)
        self._window.show()
        sys.exit(self.exec())


if __name__ == '__main__':
    app = Application()
