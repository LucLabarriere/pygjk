from pygjk.tools import Transform, Shape
from pygjk.algo import Algo
import numpy.typing as npt
import numpy as np


class Engine:
    @staticmethod
    def update(dt: float, shapes: dict[int, Shape]):
        dt = dt / 1000.0
        gravity_force = np.array([0.0, -9.81, 0.0])

        for id1, shape1 in shapes.items():
            for id2, shape2 in shapes.items():
                if id1 == id2:
                    break

                if id2 != 0:
                    break

                Algo.check_collisions(shape1, shape2)
                

        for id, shape in shapes.items():
            force = np.zeros(3, dtype=np.float32)

            if shape.rigid_body.gravity:
                force += gravity_force

            acceleration = force / shape.rigid_body.mass
            velocity_increment = acceleration * dt
            shape.rigid_body.velocity += velocity_increment

            shape.transform.translate(list(shape.rigid_body.velocity * dt))

            if shape.transform.position[1] < 0.0:
                shape.transform.position[1] = 0.0



