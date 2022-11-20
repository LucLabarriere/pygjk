from dataclasses import dataclass
import pyqtgraph as pg
import numpy as np
import random

from pygjk.tools import Shape


@dataclass
class Renderer:
    _next_id: int = 0

    def __init__(self, view):
        self._view = view
        self._scatter = pg.ScatterPlotItem(size=10)
        # self._view.addItem(self.scatter)
        self._lines = {}
        self._shapes: dict[int, Shape] = {}

    def add_shape(self, shape: Shape) -> int:
        self._shapes[self._next_id] = shape
        self._lines[self._next_id] = pg.PlotDataItem()
        self._lines[self._next_id].setPen(shape.formatted_color)
        self._view.addItem(self.lines[self._next_id])
        self._next_id += 1

        return self._next_id - 1

    def create_shape(self) -> tuple[int, Shape]:
        shape = Shape()
        id = self.add_shape(shape)

        return (id, shape)

    def create_random_shape(self) -> tuple[int, Shape]:
        id, shape = self.create_shape()

        translation = [
            random.randint(0, 4000) / 1000,
            random.randint(0, 4000) / 1000,
            0
        ]
        rotation = [
            0,
            0,
            random.randint(0, 1000) / 1000 * 360 - 180,
        ]

        scale = [
            random.randint(500, 1000) / 1000 * 0.4,
            random.randint(500, 1000) / 1000 * 0.4,
            0,
        ]
        color = [
            0,
            random.randint(10, 255),
            random.randint(10, 255),
            255,
        ]

        shape.transform.translate(translation)
        shape.transform.rotate(rotation)
        shape.transform.scale(scale)
        shape.setColor(color)

        return (id, shape)

    def get_shape(self, shape_id: int) -> Shape:
        return self._shapes[shape_id]

    @property
    def shapes(self) -> dict[int, Shape]:
        return self._shapes

    def remove_shape(self, shape_id: int) -> None:
        del self._shapes[shape_id]
        del self._lines[shape_id]

    def render(self) -> None:
        points = np.array([shape.getFormattedPoints()
                          for shape in self._shapes.values()]).flatten()
        self.scatter.setData(points)

        for id, shape in self._shapes.items():
            indices = shape.get_indices()
            points = shape.getFormattedPoints()
            sorted_points = [points[i] for i in indices]
            points = np.array([point['pos'] for point in sorted_points])

            self.lines[id].setData(points[:,0], points[:,1])
            self.lines[id].setPen(shape.formatted_color)

    @property
    def scatter(self):
        return self._scatter
    @property
    def lines(self):
        return self._lines
