import yaml

class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)

        if len(self.indents) == 1:
            super().write_line_break()


sun = {"sun":{
            "dni": 1000
            }}
material_specular = {
    "material": {
        "back": {
            "mirror": { 
                "reflectivity": 1, 
                "slope_error": 0 
                }
            }
        }
    }
material_specular["material"]["front"] = material_specular["material"]["back"]

material_black = {
    "material": {
        "back": {
            "matte": { 
                "reflectivity": 0
                }
            }
        }
    }
material_black["material"]["front"] = material_black["material"]["back"]


air_medium = {
    "medium":{
        "refractive_index":1,
        "extinction":0        
        }
    }

glass_medium = {
    "medium": air_medium["medium"]
    }

geometry_facet = {
    "geometry":[{
    "material": material_specular["material"],
    "plane": {"clip":
              [
                  {"operation": "AND",
                  "vertices": [
                      [-0.07, -0.07],
                      [-0.07, -0.07],
                      [-0.07, -0.07],
                      [-0.07, -0.07]]
                   }]
                  }
        }
        ]
        }
            

data = [
        sun,
        material_specular,
        air_medium,
        glass_medium,
        material_black,
        geometry_facet
]

with open('data.yml', 'w') as outfile:
    yaml.dump(data, outfile, Dumper=MyDumper,default_flow_style=None,sort_keys=False)
