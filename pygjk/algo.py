from pygjk.tools import *
from typing import Any


class Algo:
    _view: Any = None
    _to_plot: Any = None
    _current_plot: int = 0

    @staticmethod
    def initialize(view):
        Algo._view = view
        Algo._to_plot = [
            pg.PlotDataItem() for _ in range(10)
        ]

        for to_plot in Algo._to_plot:
            Algo._view.addItem(to_plot)

    @staticmethod
    def check_collisions(shape1: Shape, shape2: Shape) -> bool:
        Algo._current_plot = 0

        points1 = shape1.getPoints()
        points2 = shape2.getPoints()

        center1 = sum(points1) / len(points1)
        center2 = sum(points2) / len(points2)

        initial_direction = center1 - center2
        support1 = Algo.support_point(-initial_direction, points1)
        support2 = Algo.support_point(initial_direction, points2)

        # Debug rendering
        Algo.plot_vector([center2, center1])
        Algo.plot_vector([center1, support1])
        Algo.plot_vector([center2, support2])

        return False

    @staticmethod
    def support_point(direction, points):
        return points[np.argmax(np.dot(points, direction))]

    @staticmethod
    def plot_vector(vector):
        vector = np.array(vector)
        Algo._to_plot[Algo._current_plot].setData(vector[:, 0], vector[:, 1])
        Algo._current_plot += 1
