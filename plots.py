""" Used https://docs.pyvista.org/examples/00-load/read-file.html """
import pyvista as pv


def plot_obj_vtk(obj_path, vtk_path):
    pv.set_plot_theme("default")
    obj = pv.read(obj_path)
    vtk = pv.read(vtk_path)
    plotter = pv.Plotter()
    plotter.add_axes()
    plotter.add_mesh(obj, label='My Mesh', show_scalar_bar=False)
    plotter.add_mesh(vtk, label='Rays',cmap="jet", show_scalar_bar=False)
    plotter.show_bounds()
    plotter.show(cpos="xy", screenshot="obj_vtk.png")

def plot_heatmap(vtk_path):
    pv.set_plot_theme("Paraview")
    vtk = pv.read(vtk_path)
    plotter = pv.Plotter()
    plotter.add_axes()    
    plotter.show_bounds(ticks="outside")
    plotter.add_mesh(vtk,show_scalar_bar=False)
    plotter.add_scalar_bar(title="Incident flux, (W)",width=0.5,
                            position_x=0.25, position_y=0.9)
    plotter.show(cpos="xz", screenshot="heatmap.png")
    
    
obj_fpath = "export/data/shapes/Transversal_45.0_0.obj"
vtk_fpath = "export/data/shapes/Transversal_45.0_0.vtk"

# plot_obj_vtk(obj_fpath, vtk_fpath)

heatmap_vtk_fpath = "export/data/shapes/Transversal_45.0_0_heatmap.vtk"

# plot_heatmap(heatmap_vtk_fpath)