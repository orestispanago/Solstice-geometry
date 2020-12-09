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

class GeometryDescriptor:
    # HACK: Geometry entities need to hold a list of dicts
    # To be used in GeometryDAO instead of __dict__ for consistency
    def __init__(self):
        pass
    def to_dict(self):
        return self.__dict__

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
    def __init__(self, dni=1000, pillbox=None):
        self.dni = dni
        if pillbox:
            self.pillbox = pillbox.__dict__

class Pillbox(DTO):
    def __init__(self, half_angle=0.2664):
        self.half_angle = half_angle

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

class Geometry(GeometryDescriptor):
    def __init__(self, material, plane):
        self.geometry = [{"material": material_black.__dict__,
                            "plane": plane.__dict__}]

def vertices(dimx, dimy):
    x = dimx/2
    y = dimy/2
    return [[-x, -y], [-x, y], [x, y], [x, -y]]

class Template(DTO):
    def __init__(self, name, children, rotation=[0, 0, 0], translation=[0, 0, 0]):
        self.name = name
        self.transform = {"rotation":rotation, "translation": translation}
        self.children =[i.__dict__ for i in children]
    def set_translation(self, translation):
        self.transform["translation"] = translation
        return self
    def set_rotation(self, rotation):
        self.transform["rotation"] = rotation
        return self

class Entity(Template):
    def __init__(self, name, children, rotation=[0, 0, 0], translation=[0, 0, 0]):
        super(Entity, self).__init__(name, children)

sun = Sun(pillbox = Pillbox())
# sun.pillbox = Pillbox().__dict__
matte = Matte()
mirror = Mirror()
material_black = Material(matte, matte)
material_specular = Material(mirror, mirror)

receiver_vertices = vertices(0.25, 0.18)
rec_plane = Plane(Clip(receiver_vertices))
mirror_vertices = vertices(0.14, 0.7)
mirror_plane = Plane(Clip(mirror_vertices))
geometry_receiver = Geometry(material_black, rec_plane)
# {"geometry":[{"material": material_black.__dict__,
#                                   "plane": rec_plane.__dict__}]}
geometry_facet = Geometry(material_specular, mirror_plane)

# template_reflector = Template("template_reflector", children=[geometry_facet])
# template_absorber = Template("template_absorber", rotation=[0, 1.5, 0],
#                                                 children=[geometry_receiver])
# template_absorber.set_rotation([0.5, 1110, 0])
# entity_base = Entity("base", children=[template_reflector, template_absorber])
# entity_base.set_rotation([0, 14000000, 0])


y = GeometryDAO()
y.sun = sun.to_dict()
y.material_black = material_black.to_dict()
y.material_specular = material_specular.to_dict()
y.geometry_receiver = geometry_receiver.to_dict()
y.geometry_facet = geometry_facet.to_dict()
# y.template_reflector = template_reflector.to_dict()
# y.template_absorber = template_absorber.to_dict()
# y.entity_base = entity_base.to_dict()
y.write_yaml("test.yaml")

import services.solstice_run_service as solstice

obj, vtk = solstice.export_obj_vtk(180,25, geometry="test.yaml")
