class Node:
    def __init__(self):
        pass

    def to_dict(self):
        return {self.__class__.__name__.lower(): self.__dict__}


class Sun(Node):
    def __init__(self, dni=1000, pillbox=None):
        self.dni = dni
        if pillbox:
            self.pillbox = pillbox.__dict__


class Pillbox(Node):
    def __init__(self, half_angle=0.2664):
        self.half_angle = half_angle


class Matte(Node):
    def __init__(self, reflectivity=0):
        self.reflectivity = reflectivity


class Mirror(Node):
    def __init__(self, reflectivity=1, slope_error=0):
        self.reflectivity = reflectivity
        self.slope_error = slope_error


class Material(Node):
    def __init__(self, front, back):
        self.front = front.to_dict()
        self.back = back.to_dict()


class Vertices(Node):
    def __init__(self, dimx=0.7, dimy=0.7):
        self.vertices = self.vertices(dimx, dimy)


class Clip(Node):
    def __init__(self, vertices, operation="AND"):
        self.operation = operation
        self.vertices = vertices


class Plane(Node):
    def __init__(self, clip):
        self.clip = [clip.__dict__]


class Geometry(Node):
    def __init__(self, material, plane):
        self.geometry = [{"material": material.__dict__,
                          "plane": plane.__dict__}]

    def to_dict(self):
        return self.__dict__


def calc_vertices(dimx, dimy):
    x = dimx / 2
    y = dimy / 2
    return [[-x, -y], [-x, y], [x, y], [x, -y]]


class Template(Node):
    def __init__(self,
                 name,
                 primary,
                 children=None,
                 geometry=None,
                 rotation=[0, 0, 0],
                 translation=[0, 0, 0]):
        self.name = name

        self.transform = {"rotation": rotation, "translation": translation}
        if children:
            self.children = [i.__dict__ for i in children]
        else:
            self.primary = primary
        if geometry:
            self.geometry = geometry.geometry

    def set_translation(self, translation):
        self.transform["translation"] = translation
        return self

    def set_rotation(self, rotation):
        self.transform["rotation"] = rotation
        return self


class Entity(Template):
    def __init__(self,
                 name,
                 primary,
                 children=None,
                 geometry=None,
                 rotation=[0, 0, 0],
                 translation=[0, 0, 0]):
        super(Entity, self).__init__(name,
                                     primary,
                                     children,
                                     geometry,
                                     rotation,
                                     translation)
        pass
