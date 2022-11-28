from pygjk.tools import Transform, Shape
from pygjk.algo import Algo
import numpy.typing as npt
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time


class Engine:
    _update_time = 0.0

    @staticmethod
    def update(dt: float, shapes: dict[int, Shape]) -> None:
        t0 = time.time()

        dt = dt / 1000.0

        #Engine.update_multi_threaded(shapes)
        Engine.update_single_threaded(shapes)
                
        Engine._update_time = time.time() - t0

        return None

    @staticmethod
    def update_multi_threaded(shapes) -> None:
        jobs = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            for i in range(len(shapes)):
                for j in range(i + 1, len(shapes)):
                    shape1 = shapes[i]
                    shape2 = shapes[j]

                    jobs.append(executor.submit(Algo.check_collisions, shape1, shape2))

        for job in jobs:
            res = job.result()

            if res.collides:
                # Show shapes in red
                shapes[res.shape_1_id].set_color([255, 0, 0, 255])
                shapes[res.shape_2_id].set_color([255, 0, 0, 255])

    @staticmethod
    def update_single_threaded(shapes) -> None:
        collisions = []
        shapes = list(shapes.values())

        for i in range(len(shapes)):
            for j in range(i + 1, len(shapes)):
                shape1 = shapes[i]
                shape2 = shapes[j]
                collisions.append(Algo.check_collisions(shape1, shape2))

        for collision in collisions:
            if collision.collides:
                # Show shapes in red
                shapes[collision.shape_1_id].set_color([255, 0, 0, 255])
                shapes[collision.shape_2_id].set_color([255, 0, 0, 255])

    @staticmethod
    def get_update_time() -> float:
        return Engine._update_time

