from geometry import Vec3


class Camera:
    def __init__(self, v: Vec3, u: Vec3, w: Vec3, pos: Vec3, d):
        self.v = v
        self.u = u
        self.w = w
        self.pos = pos
        self.d = d


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction
