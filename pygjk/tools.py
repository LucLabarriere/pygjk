import numpy as np
import numpy.typing as npt
import copy
import pyqtgraph as pg
from scipy.spatial.transform import Rotation


class Transform:
    def __init__(self):
        self._position = np.array([1.0, 1.0, 0.0], dtype=np.float32)
        self._rotation = np.zeros(3, dtype=np.float32)
        self._scale = np.ones(3, dtype=np.float32)

    def translate(self, translation: list[float]) -> None:
        self._position += np.array(translation)

    def rotate(self, rotation: list[float]) -> None:
        self._rotation += np.array(rotation)

    def scale(self, scaling: list[float]) -> None:
        self._scale *= np.array(scaling)

    def increment_scale(self, value: list[float]) -> None:
        self._scale += np.array(value)

    def getPosition(self) -> np.ndarray:
        return self._position

    def getRotation(self) -> np.ndarray:
        return self._rotation

    def getScale(self) -> np.ndarray:
        return self._scale

    @property
    def position(self) -> np.ndarray:
        return self._position

    @position.setter
    def position(self, value) -> None:
        self._position = value


class Simplex:
    def __init__(self):
        self._points = np.zeros(3, dtype=np.float32)


class RigidBody:
    def __init__(self):
        self._mass = 1.0
        self._velocity = np.zeros(3, dtype=np.float32)
        self.gravity = False 

    @property
    def mass(self) -> float:
        return self._mass

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        self._velocity = value


class Shape:
    def __init__(self, id = 0):
        self._primitive = np.array([
            [-0.5, -0.5, 0.0],
            [-0.5, 0.5, 0.0],
            [0.5, -0.5, 0.0],
            [0.5, 0.5, 0.0]
        ])

        self.id = id
        self._transform = Transform()
        self._rigid_body = RigidBody()

        self._color = np.array([100, 100, 100, 255])
        self._is_dirty = True
        self._transformed_points = self._primitive

    def set_id(self, value):
        self.id = value

    @property
    def transform(self) -> Transform:
        return self._transform

    @property
    def rigid_body(self) -> RigidBody:
        return self._rigid_body

    def set_dirty(self):
        self._is_dirty = True

    def getPoints(self) -> npt.NDArray[np.float32]:
        if self._is_dirty:
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

            #TODO remove copy here
            new_points = copy.copy(self._primitive)
            new_points = np.concatenate((new_points, np.ones([new_points.shape[0], 1])), axis=1)
            new_points = np.dot(modelMatrix, new_points.T)
            new_points = new_points[:3].T

            #for i in range(new_points.shape[0]):
            #    new_points[i] = np.dot(
            #        modelMatrix, np.array([*new_points[i], 1]))[:3]

            self._transformed_points = new_points
            self._is_dirty = False 

        return self._transformed_points

    # TODO make work for any shape
    def get_indices(self) -> list[int]:
        return [0, 1, 3, 2, 0]

    def getFormattedPoints(self):
        return [{'pos': point, 'brush': pg.mkColor(self._color)} for point in self.getPoints()]

    @property
    def formatted_color(self):
        return pg.mkColor(self._color)

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

class Collision:
    def __init__(self, shape_1, shape_2, collides=True):
        self.shape_1_id = shape_1.id
        self.shape_2_id = shape_2.id
        self.collides = collides
