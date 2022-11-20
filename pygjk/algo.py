from numpy._typing import _UnknownType
import numpy as np
from pygjk import shapes
import matplotlib.pyplot as plt


class Algorithm:
    def __init__(self, ax, collection: list[shapes.Shape]):
        self._ax = ax
        self.stable_artists: list[_UnknownType] = []
        self.temporary_artists: list[_UnknownType] = []

        self.steps = [
            self.step_initial_direction,
            self.step_loop,
            self.step_loop,
            self.step_loop,
            self.step_loop,
            self.step_loop,
        ]

        self._shapes = collection
        self.shape_A, self.shape_B = self._shapes[0], self._shapes[1]
        self.current_step = 0

        self._fig = self._ax.figure

    def reset_figure(self):
        self._ax.clear()
        self._ax.set_xlim(-3, 4)
        self._ax.set_ylim(-3, 4)
        self._ax.figure.canvas.draw()
        self._background = self._fig.canvas.copy_from_bbox(self._ax.bbox)
        self.current_step = 0
        self.stable_artists = []
        self.temporary_artists = []

        for shape in self._shapes:
            self.stable_artists.append(self._ax.scatter(
                shape._points[:, 0], shape._points[:, 1], color=shape._color))

        self.stable_artists.append(self._ax.axvline(0, color='black'))
        self.stable_artists.append(self._ax.axhline(0, color='black'))

        minkowsky = []
        for i in range(len(self.shape_A._points)):
            for j in range(len(self.shape_B._points)):
                minkowsky.append(
                    self.shape_A._points[i] - self.shape_B._points[j])

        minkowsky = np.array(minkowsky)
        self.stable_artists.append(self._ax.scatter(
            minkowsky[:, 0], minkowsky[:, 1], color='purple'
        ))

        for artist in self.stable_artists:
            self._ax.draw_artist(artist)

        self._fig.canvas.blit(self._ax.bbox)

    def forward(self):
        print("Forwarding")
        self.steps[self.current_step]()
        self._fig.canvas.restore_region(self._background)

        for artist in self.stable_artists:
            self._ax.draw_artist(artist)

        self.current_step += 1

        for artist in self.temporary_artists:
            self._ax.draw_artist(artist)

        self._fig.canvas.blit(self._ax.bbox)

    def step_initial_direction(self):
        self.temporary_artists = []

        initial_direction = self.shape_B.center - self.shape_A.center

        self.temporary_artists.append(
            self._ax.plot([0, initial_direction[0]],
                          [0, initial_direction[1]],
                          color='black')[0])

        support_point, sA, sB = support_function(
            self.shape_A, self.shape_B, initial_direction)

        origin_points = np.array([sA, sB])
        self.temporary_artists.append(self._ax.scatter(
            origin_points[:, 0], origin_points[:, 1], color='black'
        ))

        self.temporary_artists.append(self._ax.scatter(
            support_point[0], support_point[1], color='red'))

        self.simplex = shapes.Simplex(support_point)
        self.direction = - support_point

    def step_loop(self):
        new_support_point, sA, sB = support_function(
            self.shape_A, self.shape_B, self.direction)

        origin_points = np.array([sA, sB])
        self.temporary_artists.append(self._ax.scatter(
            origin_points[:, 0], origin_points[:, 1], color='black'
        ))

        # Did it cross the origin ? If not, no collision
        if shapes.Simplex.passed_origin(new_support_point, self.direction) is False:
            return False

        self.simplex.push(new_support_point)
        self.temporary_artists.append(self._ax.scatter(
            new_support_point[0], new_support_point[1], color='red'))

        if len(self.simplex) == 2:
            print("2 points, checking line")
            result, self.direction = self.simplex.line_check(self.direction)
            points = np.array(self.simplex._points)

            self.temporary_artists.append(self._ax.plot(
                points[:, 0], points[:, 1], color='red')[0])

            if result:
                print("Colliding !!!!!")
                return True

        elif len(self.simplex) == 3:
            print("3 points, checking triangle")

            result, self.direction, origin = self.simplex.triangle_check(
                self.direction)

            self.temporary_artists.append(self._ax.plot(
                [origin[0], origin[0] - self.direction[0]],
                [origin[1], origin[1] - self.direction[1]],
                color='green'
            )[0])

            if result:
                print("Colliding (Triangle)!!")
                return True

        return False


def support_function(shape_A, shape_B, direction):
    sA = shape_A._support_function(direction)
    sB = shape_B._support_function(-direction)
    return sA - sB, sA, sB
