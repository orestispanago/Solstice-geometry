import services.plot_service as plotting
import services.solstice_run_service as solstice
from yaml_items import YamlItems
from nodes import (Sun,
                   Pillbox,
                   Matte,
                   Mirror,
                   Material,
                   Plane,
                   Clip,
                   Geometry,
                   Template,
                   Entity)
from nodes import calc_vertices

sun = Sun(pillbox=Pillbox())
# sun.pillbox = Pillbox().__dict__
matte = Matte()
mirror = Mirror()
material_black = Material(matte, matte)
material_specular = Material(mirror, mirror)

receiver_vertices = calc_vertices(0.25, 0.18)
rec_plane = Plane(Clip(receiver_vertices))
mirror_vertices = calc_vertices(0.14, 0.27)
mirror_plane = Plane(Clip(mirror_vertices))
geometry_receiver = Geometry(material_black, rec_plane)
# {"geometry":[{"material": material_black.__dict__,
#                                   "plane": rec_plane.__dict__}]}
geometry_facet = Geometry(material_specular, mirror_plane)

template_reflector = Template("template_reflector", 1,
                              geometry=geometry_facet)
template_absorber = Template("template_absorber", 0, rotation=[0, 1.5, 0],
                             children=[geometry_receiver])
# template_absorber.set_rotation([0.5, 1110, 0])
entity_reflector = Entity("reflector1", 0, rotation=[0, 90, 0],
                          geometry=geometry_facet)
entity_absorber = Entity("absorber", 1, geometry=geometry_receiver)
entity_base = Entity("base", 1, children=[entity_absorber])
# entity_base.set_rotation([0, 14000000, 0])

items = [
    sun,
    material_black,
    material_specular,
    geometry_receiver,
    geometry_facet,
    template_reflector,
    entity_reflector,
    entity_absorber,
    entity_base
]

y = YamlItems(items)

y.write_yaml("test.yaml")

obj, vtk = solstice.export_obj_vtk(180, 25, geometry="test.yaml")
plotting.plot_obj_vtk(obj, vtk)
