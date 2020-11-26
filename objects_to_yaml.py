import yaml
import json

def to_dict(obj):
    return json.loads(json.dumps(obj, default=lambda o: o.__dict__))

class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()

class Sun:
    def __init__(self,dni):
        self.dni=dni

class Property:
    def __init__(self,reflectivity, slope_error):
        self.reflectivity=reflectivity
        self.slope_error=slope_error
        
class Mirror:
    def __init__(self,reflectivity,slope_error):
        self.mirror=Property(reflectivity,slope_error)

class Matte:
    def __init__(self,reflectivity,slope_error):
       self.matte=Property(reflectivity,slope_error)   

class Material:
    def __init__(self, front, back):
        self.back=back
        self.front=front

class ClipList:
    def __init__(self,dimx, dimy):
        self.operation="AND"
        self.vertices=[
            [-dimx, -dimy],
            [-dimx, dimy],
            [dimx, dimy],
            [dimx, -dimy]
            ]

class Plane:
    def __init__(self, dimx, dimy):
        self.clip=[ClipList(dimx, dimy)]


class Geometry:
    def __init__(self, material, plane):
        self.material=material
        self.plane=plane

class Transform:
    def __init__(self,rotation, translation):
        self.rotation=rotation
        self.translation=translation

class Anchor:
    def __init__(self):
        self.name="anchor0"
        self.position=[0, 0, 0] #in the referential of the receiver

class Absorber:
    def __init__(self, name, transform, geometry):
        self.name=name
        self.primary=0
        self.transform=transform
        self.anchors=[Anchor()]
        self.geometry=geometry
        
class Children:
    def __init__(self, name, transform, geometry):
        self.name=name
        self.transform=transform,
        self.primary=1
        self.geometry=geometry
        
class Target:
    def __init__(self, absorber, anchor):
        self.anchor=f"{absorber.name}.{anchor.name}"

class ZxPivot:
    def __init__(self, ref_point, target):
        self.ref_point=ref_point
        self.target=target
        
class Template:
    def __init__(self, name, transform, zx_pivot,children):
        self.name=name
        self.transform=transform
        self.zx_pivot=zx_pivot
        self.children=[children]
        

material_specular = Material(Mirror(1,0), Mirror(0.9,0))
material_black = Material(Matte(0,0), Matte(0.1,0))
geometry_facet = Geometry(material_specular,Plane(0.7, 0.2))
geometry_absorber = Geometry(material_black, Plane(0.25, 0.23))
entity_absorber = Absorber("absorber", 
                           Transform([90, 0, 0], [0, 1.5, 0]), 
                           geometry_absorber)

entity_absorber1 = Absorber("absorber", 
                           Transform([90, 0, 0], [0, 1.5, 0]), 
                           geometry_absorber)

children = Children("facet", 
                    Transform([90, 0, 0], [0, 0, 0]), 
                    geometry_facet)
target = Target(entity_absorber, Anchor())
zx_pivot = ZxPivot([0, 0, 0], target)

template_sofacet = Template("so_facet", 
                            Transform([0, 0, 90], [0,0,0]),
                            zx_pivot,
                            children)

sun = to_dict(Sun(1000))
material_specular = to_dict(material_specular)
material_black = to_dict(material_black)
geometry_facet = to_dict(geometry_facet)
geometry_absorber = to_dict(geometry_absorber)
entity_absorber = to_dict(entity_absorber)
children = to_dict(children)
template_sofacet = to_dict(template_sofacet)

data = [
    {"sun":sun}, 
    {"material": material_specular}, 
    {"material": material_black},
    {"geometry": geometry_facet},
    {"geometry": geometry_absorber},
    {"entity": entity_absorber},
    {"template": template_sofacet},
]
with open('geometry/data.yaml', 'w') as outfile:
    yaml.dump(data, outfile, Dumper=MyDumper,default_flow_style=None,sort_keys=False)
    

