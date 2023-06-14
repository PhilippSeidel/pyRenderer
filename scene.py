from geometry import GeoObject
from geometry import Vec3
from rt import Ray
from threading import Thread
import numpy as np


def take_first(elem):
    return elem[0]


class Scene:

    def __init__(self, objects):
        self.objects = objects

    def intersects(self, ray):
        intersection_found = False
        t = float('Infinity')
        bary_a = 0
        bary_b = 0
        intersection_obj = GeoObject()
        for geoObject in self.objects:
            intersects, current_intersection_obj, current_t, current_bary_a, current_bary_b = geoObject.intersects(ray)
            if intersects:
                intersection_found = True
                if 0 < current_t < t:
                    t = current_t
                    intersection_obj = current_intersection_obj
                    bary_a = current_bary_a
                    bary_b = current_bary_b
        return intersection_found, intersection_obj, t, bary_a, bary_b

    def add_image_part(self, camera, width, height, start_x, end_x, image_parts):
        l = -width / 2
        r = width / 2
        t = height / 2
        b = -height / 2
        data = np.zeros((height, end_x - start_x, 3), dtype=np.uint8)
        for y in range(0, width):
            for x in range(start_x, end_x):
                # print("x = ", x, ", y = ", y)
                u = l + (r - l) * (x + 0.5) / width
                v = t + (b - t) * (y + 0.5) / height
                s = Vec3.scale(camera.u, u) + Vec3.scale(camera.v, v) - Vec3.scale(camera.w, camera.d)
                d = s.scale(1 / s.length())
                # print("u = ", u, ", v = ", v, ", s = ", s)
                ray = Ray(camera.pos, d)
                intersection = self.intersects(ray)
                if intersection[0]:
                    intersection_obj = intersection[1]
                    bary_a = intersection[3]
                    bary_b = intersection[4]
                    color = intersection_obj.color(bary_a, bary_b)
                    data[y][x - start_x] = [color.x1, color.x2, color.x3]
                else:
                    data[y][x - start_x] = [230, 230, 230]
        image_parts.append((start_x, data))

    def get_image(self, camera, width, height, thread_count):
        image_parts = list()
        threads = []
        width_per_thread = width // thread_count
        for i in range(thread_count):
            t = Thread(target=self.add_image_part(camera, width, height,
                                                  i * width_per_thread, (i + 1) * width_per_thread, image_parts),
                       args=[i])
            threads.append(t)
            t.start()
            print(str(t), " started")
        for t in threads:
            t.join()
            print(str(t), " joined")

        image_parts.sort(key=take_first)

        image = image_parts[0][1]
        for i in range(1, thread_count):
            image = np.concatenate((image, image_parts[i][1]), axis=1)

        return image
