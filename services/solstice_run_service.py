""" stdin can be used for all functions """

def run_to_df(geometry, cmd):
    # To be used in all run functions
    """ Run command with stdin=geometry and pipe stdout to dataframe"""
    return "dataframe"

def run_transversal(min_angle, max_angle, step, geometry, rays):
    """ Generate angle pairs
    Split angle pairs to chunks for speed
    Run solstice
    Read stdout to meaningfull dataframe """
    return "dataframe"

def run_longitudinal(min_angle, max_angle, step, geometry, rays):
    """ Generate angle pairs
    Split angle pairs to chunks for speed
    Run solstice
    Read stdout to meaningfull dataframe """
    return "dataframe"

def run_for_all_abs_pos(abs_positions, geometry, rays, aggregate):
    """ Set absorber position 
    Get dataframe from run_transversal() or run_longitudinal()
    Calculate aggregate (mean, sum etc)
    Append result to dataframe list
    Concatenate dataframe list"""
    return "concatenated dataframe list"

def run_annual_const_dni(azzen_pairs_from_df, geometry, rays, save=True):
    """ Split angle pairs to chunks for speed
    Run solstice
    Read stdout to meaningfull dataframe """
    return "dataframe"

def run_pair(azzen_list, geometry, rays):
    """ Run solstice
    Read stdout to meaningfull dataframe """
    return "dataframe"

def run_annual_real_dni(azzen_pairs_dni_from_df, geometry, rays, save=True):
    """ For each angle pair:
            set dni in geometry
    Run solstice
    Read stdout to meaningfull dataframe     
    Append result to dataframe list
    Concatenate dataframe list"""
    return "concatenated dataframe list"

def export_obj(azzen_pair_list, geometry, rays=1):
    """ Run solstice to export .obj file
    Save it and return path """
    return "obj_path"

def export_obj_vtk(azzen_pair_list, geometry, rays=100):
    """ Run solstice to export .obj and .vtk for the provided angle pair
    Save files and return paths """
    return "obj_path", "vtk_path"

def export_heatmap(azzen_pair_list, geometry, heatpath_receiver, rays=1000000):
    """ Set slices in geometry 
    Run solstice to export vtk
    save file and return path """
    return "heatmap_vtk_path"