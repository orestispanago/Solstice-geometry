import yaml
import copy
from mirror_coordinates import centered_x, centered_y
from test_geometries import export_obj_vtk, plot_obj_vtk
from traces import Transversal, Longitudinal


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()


sun = { "sun": { "dni": 1000 } }
mirror = {"mirror": { "reflectivity": 1, "slope_error": 0 }}
matte = {"matte":{ "reflectivity" : 0 }}

material_specular = {
    "material": {
        "back": mirror,
        "front": mirror
    }
}

material_black = {
    "material": {
        "back": matte,
        "front": matte
    }
}
material_black["material"]["front"] = material_black["material"]["back"]


geometry_facet = {
    "geometry":[{
    "material": material_specular["material"],
    "plane": {"clip":
              [{"operation": "AND",
                  "vertices": [
                      [-0.07, -0.07],
                      [-0.07, 0.07],
                      [0.07, 0.07],
                      [0.07, -0.07]]
                   }]
                  }
        }
        ]
        }
            
geometry_receiver = {
    "geometry": [{
    "material": material_black["material"]["back"],
      "plane":{
        "clip":[
            {
          "operation": "AND",
            "vertices": [
            [-0.125, -0.125],
            [-0.125, 0.125],
            [ 0.125, 0.125],
            [ 0.125,-0.125]
                ]
                }
            ]
          }
        }]           
}

entity_absorber = {
"entity":{
    "name": "absorber",
    "primary": 0,
    "transform": { "rotation": [0, 90, 0], "translation": [-1.5, 0, 0] },
    "anchors":[
        {
        "name": "anchor0",
        "position": [0, 0, 0] #in the referential of the receiver
            }
        ],
    "geometry": geometry_receiver["geometry"]
    }
}

template_so_facet = {
"template": {
    "name": "so_facet",
    "transform": { "rotation": [0, 0, 0] ,"translation": [0, 0, 0]},
    "zx_pivot":{
      "ref_point": [0, 0, 0],
      "target": { "anchor": entity_absorber["entity"]["name"]+\
                 "."+entity_absorber["entity"]["anchors"][0]["name"] },
        },
    "children": [
    {
      "name": "facet",
        "transform": { "rotation": [90, 0, 0], "translation": [0, 0, 0] },
        "primary": 1,
        "geometry": geometry_facet["geometry"]
        }
        ]
    }
}

entity_reflector = {
"entity":{
    "name": "reflector1",
    "transform": { "rotation": [0 ,0, 0], "translation": [ -0.750, 0, -0.450 ] },
    "children": [template_so_facet["template"]]
    }
    
}


 
yaml_items = [
        sun,
        material_specular,
        material_black,
        geometry_facet,
        geometry_receiver,
        entity_absorber,
        template_so_facet,
]

def create_reflector(entity_reflector,count ,x ,z):
    x = round(float(x),3)
    z = round(float(z),3)
    entity_reflector1 = copy.deepcopy(entity_reflector)
    entity_reflector1["entity"]["name"] =  f"reflector{count}"
    entity_reflector1["entity"]["transform"]["translation"] =[0, x, z] 
    entity_reflector1["entity"]["children"] = [template_so_facet["template"]]
    return entity_reflector1

def append_reflectors():
    count=1
    for x in centered_x:
        for y in centered_y:
            entity_reflector1 = create_reflector(entity_reflector,count, x, y)
            yaml_items.append(entity_reflector1)    
            count+=1

def write_yaml(yaml_items):    
    with open('geometry/data.yaml', 'w') as outfile:
        yaml.dump(yaml_items, outfile, Dumper=MyDumper,default_flow_style=None,
                  sort_keys=False)


def set_absorber_rotation(rotation):
    entity_absorber["entity"]["transform"]["rotation"] = rotation
    
def set_absorber_translation(translation):
    entity_absorber["entity"]["transform"]["translation"] = translation

def set_template_so_facet_rotation(rotation):
    template_so_facet["template"]["transform"]["rotation"] = rotation

def set_template_so_facet_children_rotation(rotation):
    template_so_facet["template"]["children"][0]["transform"]["rotation"] = rotation
# set_absorber_rotation([0, 90, 0])
# set_absorber_translation([-1.5, 0, 0])
# set_template_so_facet_rotation([0, 0, 0])
# set_template_so_facet_children_rotation([90, 0, 0])
append_reflectors()
write_yaml(yaml_items)

# obj, vtk = export_obj_vtk(180,25)
# plot_obj_vtk(obj, vtk)


long = Longitudinal(0, 45, 1, 10000, "data.yaml")
tr_df = long.run_to_df()
tr_df = tr_df.set_index("zenith")
tr_df["missing_losses"].plot()