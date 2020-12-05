import yaml
import copy
import numpy as np
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
entity_all = {
"entity":{
    "name": "all_reflectors",
    "transform": { "rotation": [0 ,0, 0], "translation": [ 0, 0, 0 ] },
    "children": []
    }
    
}
template_reflector = {
"template":{
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

def set_tilt(tilt):
    focal_length = 1.5
    z_abs = float(focal_length * np.cos(np.deg2rad((90-tilt))))
    x_abs = float(-focal_length * np.sin(np.deg2rad((90-tilt))))
    entity_absorber["entity"]["transform"]["rotation"] = [0, -(90-tilt), 0]
    entity_absorber["entity"]["transform"]["translation"] = [x_abs, 0, z_abs]
    entity_all["entity"]["transform"]["rotation"] = [0, tilt, 0] 

def create_reflector(entity_reflector,count ,y ,z):
    y = round(float(y),3)
    z = round(float(z),3)
    template_ref = copy.deepcopy(template_reflector)
    template_ref["template"]["name"] =  f"reflector{count}"
    template_ref["template"]["transform"]["translation"] =[0, y, z] 
    template_ref["template"]["children"] = [template_so_facet["template"]]
    return template_ref

def append_reflectors():
    count=1
    for x in centered_x:
        for y in centered_y:
            template_ref = create_reflector(template_reflector,count, x, y)
            yaml_items.append(template_ref)
            entity_all["entity"]["children"].append(template_ref["template"])
            count+=1
    yaml_items.append(entity_all)

def write_yaml(yaml_items):    
    with open('geometry/data.yaml', 'w') as outfile:
        yaml.dump(yaml_items, outfile, Dumper=MyDumper,default_flow_style=None,
                  sort_keys=False)



# set_tilt(45)
append_reflectors()
write_yaml(yaml_items)


obj, vtk = export_obj_vtk(180,25)
plot_obj_vtk(obj, vtk)


# transv = Transversal(180, 225, 1, 100000, "data.yaml")
# tr_df = transv.run_to_df()
# transv.export_vtk(nrays=1000)
# transv.export_objs()
# tr_df = tr_df.set_index("azimuth")
# tr_df["shadow_losses"].plot()