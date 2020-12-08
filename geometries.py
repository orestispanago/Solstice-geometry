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


class BaseGeometry:
    def __init__(self, sun={"sun": {"dni": 1000}},
                 material_black={
            "material": {
                "back": {"matte":
                             {"reflectivity": 0}
                         },
                "front": {"matte":
                              {"reflectivity": 0}
                          }
            }
        },
        ):
        self.sun = sun
        self.material_black = material_black
        self.material_specular = {
            "material": {
                "back": {"mirror": {"reflectivity": 1,
                                    "slope_error": 0}
                         },
                "front": {"mirror": {"reflectivity": 1,
                                     "slope_error": 0}
                          },
            }
        }
        self.geometry_facet = {
            "geometry": [{
                "material": self.material_specular["material"],
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
        self.geometry_receiver = {
            "geometry": [{
                "material": self.material_black["material"]["back"],
                "plane": {
                    "clip": [
                        {
                            "operation": "AND",
                            "vertices": [
                                [-0.125, -0.125],
                                [-0.125, 0.125],
                                [0.125, 0.125],
                                [0.125, -0.125]
                            ]
                        }
                    ]
                }
            }]
        }
        self.entity_base = {
            "entity":
                {"name": "base",
                "transform":
                  {"rotation": [0, 45, 0],
                  "translation": [0, 0, 0]},
                "children":
                [{"name": "absorber",
                  "primary": 0,
                  "transform":
                    {"rotation": [0, 90, 0],
                    "translation": [-1.5, 0, 0]},
                  "anchors":
                  [{"name": "anchor0",
                    "position": [0, 0, 0]},
                  {"geometry": self.geometry_receiver["geometry"]}
                ]}]}}
        # self.entity_absorber = {
        #     "entity": {
        #         "name": "absorber",
        #         "primary": 0,
        #         "transform": {"rotation": [0, 90, 0],
        #                       "translation": [-1.5, 0, 0]},
        #         "anchors": [
        #             {
        #                 "name": "anchor0",
        #                 "position": [0, 0, 0]  # in the referential of the receiver
        #             }
        #         ],
        #         "geometry": self.geometry_receiver["geometry"]
        #     }
        # }
        self.template_so_facet = {
            "template": {
                "name": "so_facet",
                "transform": {"rotation": [0, 0, 0],
                              "translation": [0, 0, 0]},
                "zx_pivot": {
                    "ref_point": [0, 0, 0],
                    "target": {"anchor":
                                   self.entity_absorber["entity"]["name"] + \
                   "." + self.entity_absorber["entity"]["anchors"][0]["name"]},
                },
                "children": [
                    {
                        "name": "facet",
                        "transform": {"rotation": [90, 0, 0],
                                      "translation": [0, 0, 0]},
                        "primary": 1,
                        "geometry": self.geometry_facet["geometry"]
                    }]}}
        self.template_reflector = {
            "template": {
                "name": "template_reflector1",
                "transform": {"rotation": [0, 0, 0],
                              "translation": [0, 0, 0]},
                "children": [
                    self.template_so_facet["template"]]
            }

        }
        self.entity_all = {
            "entity": {
                "name": "all_reflectors",
                "transform": {"rotation": [0, 0, 0],
                              "translation": [0, 0, 0]},
                "children": []
            }
        }
        self.append_reflectors()

    def create_reflector(self, count, y, z):
        y = round(float(y), 3)
        z = round(float(z), 3)
        template_ref = copy.deepcopy(self.template_reflector)
        template_ref["template"]["name"] = f"reflector{count}"
        template_ref["template"]["transform"]["translation"] = [0, y, z]
        template_ref["template"]["children"] = \
            [self.template_so_facet["template"]]
        return template_ref

    def append_reflectors(self):
        count = 1
        for x in centered_x:
            for y in centered_y:
                template_ref = self.create_reflector(count, x, y)
                self.entity_all["entity"]["children"]. \
                    append(template_ref["template"])
                count += 1
        return self

    def set_tilt(self, tilt):
        focal_length = 1.5
        z_abs = float(focal_length * np.cos(np.deg2rad((90 - tilt))))
        x_abs = float(-focal_length * np.sin(np.deg2rad((90 - tilt))))
        self.entity_absorber["entity"]["transform"]["rotation"] = \
            [0, -(270 - tilt), 0]
        self.entity_absorber["entity"]["transform"]["translation"] = \
            [x_abs, 0, z_abs]
        self.entity_all["entity"]["transform"]["rotation"] = [0, tilt, 0]
        return self

    def plane_vertices(self, len_x, len_y):
        x = len_x / 2
        y = len_y / 2
        return [[-x, -y], [-x, y], [x, y], [x, -y]]

    def set_absorber_vertices(self, len_x, len_y):
        self.geometry_receiver["geometry"][0]["plane"]["clip"][0]["vertices"] = \
            self.plane_vertices(len_x, len_y)
        return self

    def set_facet_vertices(self, len_x, len_y):
        self.geometry_facet["geometry"][0]["plane"]["clip"][0]["vertices"] = \
            self.plane_vertices(len_x, len_y)
        return self

    def to_list(self):
        return [getattr(self, key) for key in self.__dict__.keys()]

    def write_yaml(self, fpath):
        with open(fpath, 'w') as outfile:
            yaml.dump(self.to_list(), outfile, Dumper=MyDumper,
                      default_flow_style=None, sort_keys=False)


bg = BaseGeometry()

tg = BaseGeometry().set_tilt(45)

tg.write_yaml('geometry/data1.yaml')
obj, vtk = export_obj_vtk(180, 25)
plot_obj_vtk(obj, vtk)

# transv = Transversal(180, 225, 1, 100000, "data.yaml")
# tr_df = transv.run_to_df()

# tg.write_yaml('geometry/data.yaml')
# obj, vtk = export_obj_vtk(180, 25)
# plot_obj_vtk(obj, vtk)
#
# bg.write_yaml('geometry/data.yaml')
#
# obj, vtk = export_obj_vtk(180, 25)
# plot_obj_vtk(obj, vtk)
