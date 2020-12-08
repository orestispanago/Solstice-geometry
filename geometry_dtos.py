import yaml

class GeometryDAO:
    def __init__(self):
        pass
    
    def to_list(self):
        return [getattr(self, key) for key in self.__dict__.keys()]
    
    def write_yaml(self, fpath):
        with open(fpath, 'w') as outfile:
            yaml.dump(self.to_list(), outfile, Dumper=MyDumper,
                      default_flow_style=None, sort_keys=False)


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

class DTO:
    def __init__(self):
        pass
    def to_dict(self):
        return {self.__class__.__name__.lower() : self.__dict__}
    
    
class Sun(DTO):
    def __init__(self, dni=1000, pillbox=0):
        self.dni = dni
        self.pillbox = {"half_angle" : pillbox}

class Matte(DTO):
    def __init__(self, reflectivity=0):
        self.reflectivity = reflectivity

class Mirror(DTO):
    def __init__(self, reflectivity=1, slope_error=0):
        self.reflectivity = reflectivity
        self.slope_error = slope_error

class Material(DTO):
    def __init__(self, front, back):
        self.front = front.to_dict()
        self.back = back.to_dict()   

class Vertices(DTO):
    def __init__(self, dimx=0.7, dimy=0.7):
        self.vertices = self.vertices(dimx, dimy)

    
class Clip(DTO):
    def __init__(self, vertices, operation="AND"):
        self.operation = operation
        self.vertices = vertices

class Plane(DTO):
    def __init__(self, clip):
        self.clip = [clip.__dict__]

class Geometry(DTO):
    def __init__(self, material, plane):
        self.material = material.__dict__
        self.plane = plane.__dict__
        
def vertices(dimx, dimy):
    x = dimx/2
    y = dimy/2
    return [[-x, -y], [-x, y], [x, y], [x, -y]]      


sun = Sun()
matte = Matte()
mirror = Mirror()
material_black = Material(matte, matte)
material_specular = Material(mirror, mirror)

receiver_vertices = vertices(0.25, 0.18)
rec_plane = Plane(Clip(receiver_vertices))
mirror_vertices = vertices(0.14, 0.7)
mirror_plane = Plane(Clip(mirror_vertices))
geometry_receiver = Geometry(material_black, rec_plane)
geometry_facet = Geometry(material_specular, mirror_plane)


y = GeometryDAO()
y.sun = sun.to_dict()
y.material_black = material_black.to_dict()
y.material_specular = material_specular.to_dict()
y.geometry_receiver = geometry_receiver.to_dict()
y.geometry_facet = geometry_facet.to_dict()
y.write_yaml("test.yaml")