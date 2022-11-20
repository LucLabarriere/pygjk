from dataclasses import dataclass
import numpy as np
import copy
import pyqtgraph as pg
from scipy.spatial.transform import Rotation


@dataclass
class Transform:
    _position = np.zeros(3, dtype=np.float32)
    _rotation = np.zeros(3, dtype=np.float32)
    _scale = np.ones(3, dtype=np.float32)

    def translate(self, translation: list[float]) -> None:
        self._position += np.array(translation)

    def rotate(self, rotation: list[float]) -> None:
        self._rotation += np.array(rotation)

    def scale(self, scaling: list[float]) -> None:
        self._scale += np.array(scaling)

    def getPosition(self) -> np.ndarray:
        return self._position

    def getRotation(self) -> np.ndarray:
        return self._rotation

    def getScale(self) -> np.ndarray:
        return self._scale


@dataclass
class Simplex:
    _points = np.zeros(3, dtype=np.float32)


@dataclass
class Shape:
    _primitive = np.array([
        [-0.5, -0.5, 0.0],
        [-0.5, 0.5, 0.0],
        [0.5, -0.5, 0.0],
        [0.5, 0.5, 0.0]
    ])

    _transform = Transform()

    _color = np.array([100, 100, 100, 255])

    @property
    def transform(self) -> Transform:
        return self._transform

    def getPoints(self) -> np.ndarray:
        modelMatrix = np.ones((4, 4))

        modelMatrix = Transformations.scale(
            self._transform.getScale(), modelMatrix
        )
        modelMatrix = Transformations.rotate(
            self._transform.getRotation(), modelMatrix
        )
        modelMatrix = Transformations.translate(
            self._transform.getPosition(), modelMatrix
        )

        new_points = copy.copy(self._primitive)

        for i in range(new_points.shape[0]):
            new_points[i] = np.dot(
                modelMatrix, np.array([*new_points[i], 1]))[:3]

        return new_points

    def getFormattedPoints(self):
        return [{'pos': point, 'brush': pg.mkColor(self._color)} for point in self.getPoints()]

    def setColor(self, rgba: list[int]) -> None:
        self._color = np.array(rgba)


class Transformations:
    @staticmethod
    def translate(vec3: np.ndarray, mat4: np.ndarray):
        translationMatrix = np.zeros((4, 4))
        np.fill_diagonal(translationMatrix, 1.0)
        translationMatrix[0, 3] = vec3[0]
        translationMatrix[1, 3] = vec3[1]
        translationMatrix[2, 3] = vec3[2]

        mat4 = np.dot(translationMatrix, mat4)
        return mat4

    @staticmethod
    def rotate(vec3: np.ndarray, mat4: np.ndarray):
        rot = Rotation.from_euler('xyz', np.deg2rad(vec3))
        mat4[:3][:, :3] = np.dot(rot.as_matrix(),  mat4[:3][:, :3])

        return mat4

    @staticmethod
    def scale(vec3: np.ndarray, mat4: np.ndarray):
        scalingMatrix = np.zeros((4, 4))
        np.fill_diagonal(scalingMatrix, np.array([*vec3, 1]))

        mat4 = scalingMatrix * mat4

        return mat4
