from pygjk.tools import *
from typing import Any


class Algo:
    _view: Any = None
    _lines_to_plot: Any = None
    _dots_to_plot: Any = None
    _minkowsky_to_plot: Any = None
    _simplex_to_plot: Any = None
    _current_plot: int = 0

    @staticmethod
    def initialize(view):
        Algo._view = view

        Algo._lines_to_plot = [
            pg.PlotDataItem() for _ in range(10)
        ]

        Algo._dots_to_plot = [
            pg.ScatterPlotItem() for _ in range(10)
        ]

        Algo._minkowsky_to_plot = pg.ScatterPlotItem()
        Algo._minkowsky_to_plot.setBrush(pg.mkColor([255, 0, 0, 255]))

        Algo._simplex_to_plot = [ pg.PlotDataItem() for _ in range(3) ]

        for to_plot in Algo._simplex_to_plot:
            to_plot.setPen(pg.mkColor([255, 0, 0, 255]))

        for to_plot in Algo._lines_to_plot:
            Algo._view.addItem(to_plot)

        for to_plot in Algo._dots_to_plot:
            Algo._view.addItem(to_plot)

        Algo._view.addItem(Algo._minkowsky_to_plot)

        for to_plot in Algo._simplex_to_plot:
            Algo._view.addItem(to_plot)

    @staticmethod
    def reset_data() -> None:
        Algo._current_plot = 0

        for line in Algo._lines_to_plot:
            line.setData([0], [0])

        for dots in Algo._dots_to_plot:
            dots.setData([0], [0])

        for simplex in Algo._simplex_to_plot:
            simplex.setData([0], [0])

    @staticmethod
    def check_collisions(shape_1: Shape, shape_2: Shape) -> bool:
        Algo.reset_data()

        points_1 = shape_1.getPoints()
        points_2 = shape_2.getPoints()

        center_1 = Algo.center(points_1)
        center_2 = Algo.center(points_2)

        direction = Algo.normalize(center_1 - center_2)
        support = Algo.support(direction, points_1, points_2)

        simplex = [support]
        direction = - support

        while True:
            new_support = Algo.support(direction, points_1, points_2)

            simplex.append(new_support)

            if Algo.crossed_origin(new_support, direction) == False:
                return Algo.does_not_collide(shape_1, shape_2)

            result, direction = Algo.handle_simplex(simplex, direction)
            if result:
                return Algo.collides(shape_1, shape_2)


    @staticmethod
    def handle_simplex(simplex, direction):
        if len(simplex) == 2:
            return Algo.handle_line_simplex(simplex, direction)

        return Algo.handle_triangle_simplex(simplex, direction)

    @staticmethod
    def handle_line_simplex(simplex, direction):
        B, A = simplex
        AB, AO = B - A, - A
        ABperp = Algo.triple_product(AB, AO, AB)
        direction = ABperp

        return False, direction

    @staticmethod
    def handle_triangle_simplex(simplex, direction):
        C, B, A = simplex
        AB, AC, AO = B - A, C - A, - A
        ABperp = Algo.triple_product(AC, AB, AB)
        ACperp = Algo.triple_product(AB, AC, AC)

        if np.dot(ABperp, AO) > 0:  # Region AB
            del simplex[0]
            direction = Algo.normalize(ABperp)
            return False, direction

        if np.dot(ACperp, AO) > 0:  # Region AC
            del simplex[1]
            direction = Algo.normalize(ACperp)
            return False, direction

        return True, direction

    @staticmethod
    def does_not_collide(shape_1, shape_2):
        return False

    @staticmethod
    def collides(shape_1, shape_2):
        shape_1.setColor([255, 0, 0, 255])
        shape_2.setColor([255, 0, 0, 255])
        return True 

    @staticmethod
    def crossed_origin(point, direction):
        return np.dot(point, direction) > 0

    @staticmethod
    def origin():
        return np.zeros(3, dtype=np.float32)

    @staticmethod
    def normalize(vector):
        return vector / np.linalg.norm(vector)

    @staticmethod
    def center(points):
        return sum(points) / len(points)

    @staticmethod
    def furthest_point(direction, points):
        furthest = points[np.argmax(np.dot(points, direction))]
        return furthest

    @staticmethod
    def support(direction, points_1, points_2):
        furthest_1 = Algo.furthest_point(-direction, points_1)
        furthest_2 = Algo.furthest_point(direction, points_2)

        return furthest_2 - furthest_1

    @staticmethod
    def plot_vector(vector):
        vector = np.array(vector)

        Algo._lines_to_plot[Algo._current_plot].setData(vector[:, 0], vector[:, 1])
        Algo._dots_to_plot[Algo._current_plot].setData([vector[1][0]], [vector[1][1]], symbol='x')
        Algo._current_plot += 1

    @staticmethod
    def plot_simplex(simplex):
        for i in range(len(simplex)):
            a = simplex[i - 1]
            b = simplex[i]
            points = np.array([a, b])

            Algo._simplex_to_plot[i - 1].setData(points[:,0], points[:,1])

    @staticmethod
    def plot_minkowsky(points_1, points_2):
        minkowsky_difference = []

        for point_1 in points_1:
            for point_2 in points_2:
                minkowsky_difference.append(point_2 - point_1)

        minkowsky_difference = np.array(minkowsky_difference)

        Algo._minkowsky_to_plot.setData(minkowsky_difference[:,0], minkowsky_difference[:,1], symbol='o')

    @staticmethod
    def triple_product(a, b, c):
        return np.cross(np.cross(a, b), c)
