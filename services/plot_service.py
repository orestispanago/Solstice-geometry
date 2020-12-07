def plot_geometry_quantities(df, columns_list):
    """ Plots columns of dataframe in separate figures """
    
def plot_geometries_comparison(df, column):
    """ Plots same column name from different dataframes in one figure """

def plot_calendar_heatmap(df, column):
    """ Resample and pivot dataframe
    Plot calendar heatmap, x=date, y= time """

def plot_heatmap(df, column):
    """ Pivot dataframe containing absorber positions
    Plot heatmap """


""" Pyvista """

def plot_obj(obj_path):
    """ Plot .obj file """

def plot_obj_vtk(obj_path, vtk_path):
    """ Plot .obj ant .vtk in same window """
    
def plot_flux_distribution(heatmap_vtk_path):
    """ Plot flux didtribution from vtk_path """
    
    
    
    
""" Optional """
def plot_mirror_coordinates(centered_x, centered_y):
    """ Creates meshgrid from centered_x, centered_y and plots them and 0(0,0)"""
