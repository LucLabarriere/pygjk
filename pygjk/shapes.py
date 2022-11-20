from __future__ import annotations
import numpy as np


class Shape:
    def __init__(self, points: np.ndarray, color='black', ax=None):
        self._points: np.ndarray = points
        self._color = color
        self._ax = ax

    @property
    def center(self) -> np.ndarray:
        return np.sum(self._points, axis=0) / len(self._points)

    def _support_function(self, direction: np.ndarray) -> np.ndarray:
        argument = np.argmax(np.dot(self._points, normalize(direction)))
        pos = self._points[argument]

        return pos

    def check_collision(self, other: Shape) -> bool:
        initial_direction = normalize(self.center - other.center)
        support_point = self._support_function(initial_direction)

        simplex = Simplex(support_point)
        direction = - support_point

        while True:
            new_support_point = self._support_function(direction)

            # Did it cross the origin ? If not, no collision
            if Simplex.passed_origin(new_support_point, direction) is False:
                return False

            simplex.push(new_support_point)

            if len(simplex) == 2:
                if simplex.line_check(direction):
                    return True
            elif len(simplex) == 3:
                if simplex.triangle_check(direction):
                    return True
            else:  # 4
                simplex.tetrahedron_check()

    def draw(self) -> None:
        if self._ax != None:
            self._ax.scatter(self._points[:, 0],
                             self._points[:, 1], color=self._color)

    def draw_direction(self, direction) -> None:
        if self._ax != None:
            self._ax.plot([self.center[0], self.center[0] + direction[0]],
                          [self.center[1], self.center[1] + direction[1]], color=self._color)

    def draw_support_point(self, direction) -> None:
        if self._ax != None:
            p = self._support_function(direction)
            self._ax.scatter(p[0], p[1], color='red')


class Simplex:
    def __init__(self, first_point):
        self._points = [first_point]

    def push(self, point: np.ndarray) -> None:
        self._points.append(point)

    def __len__(self) -> int:
        return len(self._points)

    def line_check(self, direction: np.ndarray):
        A, B = self._points[0], self._points[1]
        AB, AO = B - A, - A
        ABperpendicular = triple_product(AB, AO)
        print(f"AB: {AB}, AO: {AO}, Perpendicular: {ABperpendicular}")
        direction = ABperpendicular

        return np.dot(AO, direction) == 0, direction

    def triangle_check(self, direction: np.ndarray):
        A, B, C = self._points
        AB, AC, AO = B - A, C - A, - A

        ABperpendicular = normalize(-triple_product(AB, AO))
        ACperpendicular = normalize(-triple_product(AC, AO))

        print(f"AB: {AB}, AO: {AO}, Perpendicular: {ABperpendicular}")

        if np.dot(ABperpendicular, AO) > 0:  # Region AB
            print("Region AB")
            del self._points[-1]
            direction = ABperpendicular
            origin = (A + B) / 2

            return False, direction, origin

        if np.dot(ACperpendicular, AO) > 0:  # Region AC
            print("Region AC")
            del self._points[-2]
            direction = ACperpendicular
            origin = (A + C) / 2

            return False, direction, origin

        return True, direction, np.array([0.0, 0.0, 0.0]) 

    def tetrahedron_check(self) -> bool:
        return False

    @staticmethod
    def passed_origin(support_point: np.ndarray, direction: np.ndarray) -> None:
        return np.dot(support_point, direction) > 0


def triple_product(AB: np.ndarray, AO: np.ndarray) -> np.ndarray:
    return np.cross(np.cross(AB, AO), AB)


def normalize(vector: np.ndarray) -> np.ndarray:
    return vector / np.linalg.norm(vector)
