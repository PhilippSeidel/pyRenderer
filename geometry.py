import numpy as np
import math


class Vec3:
    def __init__(self, x1, x2, x3):
        self.x1 = x1
        self.x2 = x2
        self.x3 = x3

    def __add__(self, other):
        return Vec3(self.x1 + other.x1, self.x2 + other.x2, self.x3 + other.x3)

    def __sub__(self, other):
        return Vec3(self.x1 - other.x1, self.x2 - other.x2, self.x3 - other.x3)

    def __str__(self):
        return "[" + str(self.x1) + ", " + str(self.x2) + ", " + str(self.x3) + "]"

    def scale(self, scalar):
        return Vec3(self.x1 * scalar, self.x2 * scalar, self.x3 * scalar)

    def length(self):
        return math.sqrt(math.pow(self.x1, 2) + math.pow(self.x2, 2) + math.pow(self.x3, 2))


class GeoObject:
    def intersects(self, ray):
        return False, self, 0, 0, 0

    def color(self, bary_ab, bary_ac):
        return Vec3(0, 0, 0)


class Triangle(GeoObject):
    def __init__(self, a: Vec3, b: Vec3, c: Vec3, col_a: Vec3, col_b: Vec3, col_c: Vec3):
        self.a = a
        self.b = b
        self.c = c
        self.col_a = col_a
        self.col_b = col_b
        self.col_c = col_c

    def intersects(self, ray):
        x = self.b - self.a
        y = self.c - self.a
        m = np.array([[ray.direction.x1, -x.x1, -y.x1],
                     [ray.direction.x2, -x.x2, -y.x2],
                     [ray.direction.x3, -x.x3, -y.x3]])

        det_m = np.linalg.det(m)

        if -0.001 < det_m < 0.001:
            return False, 0, 0, 0, 0

        m1 = np.array([[self.a.x1 - ray.origin.x1, -x.x1, -y.x1],
                      [self.a.x2 - ray.origin.x2, -x.x2, -y.x2],
                      [self.a.x3 - ray.origin.x3, -x.x3, -y.x3]])

        m2 = np.array([[ray.direction.x1, self.a.x1 - ray.origin.x1, -y.x1],
                      [ray.direction.x2, self.a.x2 - ray.origin.x2, -y.x2],
                      [ray.direction.x3, self.a.x3 - ray.origin.x3, -y.x3]])

        m3 = np.array([[ray.direction.x1, -x.x1, self.a.x1 - ray.origin.x1],
                      [ray.direction.x2, -x.x2, self.a.x2 - ray.origin.x2],
                      [ray.direction.x3, -x.x3, self.a.x3 - ray.origin.x3]])

        det_m2 = np.linalg.det(m2)
        det_m3 = np.linalg.det(m3)
        bary_ab = det_m2 / det_m
        bary_ac = det_m3 / det_m

        # print("bary_ab = ", bary_ab, ", bary_ac = ", bary_ac)
        # print("o = ", ray.origin, ", d = ", ray.direction, "\n")

        if bary_ab < 0 or bary_ac < 0 or bary_ab + bary_ac > 1:
            return False, self, 0, 0, 0

        det_m1 = np.linalg.det(m1)
        t = det_m1 / det_m

        return True, self, t, bary_ab, bary_ac

    def color(self, bary_ab, bary_ac):
        return self.col_a.scale(1 - bary_ab - bary_ac) + self.col_b.scale(bary_ab) + self.col_c.scale(bary_ac)
