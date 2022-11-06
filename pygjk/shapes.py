from __future__ import annotations
import numpy as np


class Shape:
    def __init__(self, points: np.ndarray, color='black'):
        self._points: np.ndarray = points
        self._color = color

    @property
    def center(self) -> np.ndarray:
        return np.sum(self._points) / len(self._points)

    def _support_function(self, direction: np.ndarray) -> np.ndarray:
        argument = np.argmax(np.dot(self._points, direction))
        pos = self._points[argument]

        return pos

    def check_collision(self, other: Shape) -> bool:
        print("Checking collisions")
        return False

    def draw(self, ax) -> None:
        ax.scatter(self._points[:, 0], self._points[:, 1], color=self._color)

    def draw_direction(self, direction, ax) -> None:
        ax.plot([self.center[0], self.center[0] + direction[0]],
                [self.center[1], self.center[1] + direction[1]], color=self._color)

    def draw_support_point(self, direction, ax) -> None:
        p = self._support_function(direction)
        ax.scatter(p[0], p[1], color='red')
