from pygjk.tools import *
from typing import Any


class Algo:
    @staticmethod
    def check_collisions(shape_1: Shape, shape_2: Shape) -> Collision:
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
                return Collision(shape_1, shape_2, False)

            result, direction = Algo.handle_simplex(simplex, direction)

            if result:
                return Collision(shape_1, shape_2)

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
    def triple_product(a, b, c):
        return np.cross(np.cross(a, b), c)
