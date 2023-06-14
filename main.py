from PIL import Image
from scene import Scene
from rt import Camera
from geometry import Triangle
from geometry import Vec3
import time


def render_image(img_array):
    img = Image.fromarray(img_array)  # Create a PIL image
    img.show()  # View in default viewer


if __name__ == '__main__':

    width = 256
    height = 256

    camera = Camera(Vec3(1, 0, 0), Vec3(0, 1, 0), Vec3(0, 0, -1), Vec3(0, 0, -10), 2)
    scene = Scene([Triangle(Vec3(-500, -500, 0), Vec3(-250, 250, 0), Vec3(250, -250, 0),
                            Vec3(254, 0, 0), Vec3(254, 0, 0), Vec3(254, 0, 0)),
                   Triangle(Vec3(250, -250, 0), Vec3(500, 500, 30), Vec3(-250, 250, 0),
                            Vec3(0, 254, 0), Vec3(0, 254, 0), Vec3(0, 254, 0))])
    img_array = scene.get_image(camera, width, height, 1)
    render_image(img_array)
