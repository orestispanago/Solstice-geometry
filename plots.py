""" Used https://docs.pyvista.org/examples/00-load/read-file.html """
import pyvista as pv

obj = pv.read("export/data/shapes/Transversal_45.0_0.obj")
rays = pv.read("export/data/shapes/Transversal_45.0_0.vtk")
# mesh2 = pv.read("export/data/shapes/Transversal_45.0_0_heatmap.vtk")
plotter = pv.Plotter()
plotter.add_mesh(obj)
plotter.add_mesh(rays, cmap="jet")
# plotter.add_mesh(mesh2,show_scalar_bar=False)
plotter.show(cpos="xy", screenshot="myscreenshot.png")