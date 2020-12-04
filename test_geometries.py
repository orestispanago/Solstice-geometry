import os
import subprocess
import pyvista as pv
import utils



        
def export_obj_vtk(az, zen):
    utils.mkdir_if_not_exists("out")
    pairs = f"{az:.1f},{zen:.1f}"
    objpath = os.path.join("out", pairs + ".obj")
    vtkpath = os.path.join("out", pairs+ ".vtk")
    obj_cmd = f'solstice  -n 100 -g format=obj -t1 -D {pairs} -R {receiver} {geometry}'.split()
    vtk_cmd = f'solstice  -n 100 -p default -t1 -D {pairs} -R {receiver} {geometry}'.split()
    with open(objpath, 'w') as o:
        subprocess.run(obj_cmd, stdout=o)
    with open(vtkpath, 'w') as v:
            subprocess.run(vtk_cmd, stdout=v)
    utils.del_first_line(vtkpath)    
    return objpath, vtkpath

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
   
receiver = "geometry/receiver.yaml"
geometry = "geometry/data.yaml"

# obj, vtk = export_obj_vtk(45,0)
# plot_obj_vtk(obj, vtk)

