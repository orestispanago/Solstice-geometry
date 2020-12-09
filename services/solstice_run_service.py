""" stdin can be used for all functions """
from subprocess import PIPE, Popen, run
from io import StringIO
import numpy as np
from tqdm import tqdm
import os
import pandas as pd
import utils

receiver = os.path.join(os.getcwd(), "geometry", "receiver.yaml")

def run_to_df(geometry, cmd):
    """ Run command with stdin=geometry and pipe stdout to dataframe"""
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(input=geometry.encode())
    b = StringIO(out.decode())
    return read(b)

def run_chunks(angle_pairs, geometry, rays):
    df_list = []
    # Solstice cannot take too long string of angle arguments, so split into chunks
    for i in tqdm(range(0, len(angle_pairs), 20)):
        chunk = angle_pairs[i:i + 20]
        chunk = ":".join(chunk)
        cmd = f'solstice -D {chunk} -n {rays} -v -R {receiver}'.split()
        df = run_to_df(geometry, cmd)
        df_list.append(df)
    return pd.concat(df_list)

def run_transversal(geometry, min_angle=180, max_angle=225, step=1, rays=10000):
    angles = np.arange(min_angle, max_angle + 1, step) # TODO check if tolist() is necessary
    angle_pairs = [f"{a:.1f},0" for a in angles]
    return run_chunks(angle_pairs, geometry, rays)

def run_longitudinal(geometry, min_angle=0, max_angle=25, step=0.5, rays=10000):
    angles = np.arange(min_angle, max_angle + 1, step).tolist()
    angle_pairs = [f"180,{a:.1f}" for a in angles]
    return run_chunks(angle_pairs, geometry, rays)


def abs_positions(coords):
    # step = config.direction.absorber_shift_step
    step = 0.2
    return np.arange(round(coords[0], 1), round(coords[-1], 1) + 0.0001, step)


def run_for_all_abs_pos(abs_positions, geometry, rays, aggregate):
    """ Set absorber position
    Get dataframe from run_transversal() or run_longitudinal()
    Calculate aggregate (mean, sum etc)
    Append result to dataframe list

    Concatenate dataframe list"""    """ Changes absorber position,
    runs direction with output to dataframe (as Direction class attribute),
    calculates aggregate of dataframe columns (sum, mean, etc)
    returns new dataframe with coords and columns aggregate """
    columns = {
       "potential_flux": 2,
       "absorbed_flux": 3,
       "cos_factor": 4,
       "shadow_losses": 5,
       "missing_losses": 6,
       # "reflectivity_losses": 7,
       # "absorptivity_losses": 8
       }
    cols = ["efficiency", *columns.keys()]
    df = pd.DataFrame(columns=["abs_x", "abs_y", *cols])
    for x in tqdm(abs_positions(centered_x)):
        for y in abs_positions(centered_y):
            geometry = geometry.set_abs_pos(x, y)
            tr_df = run_transversal(geometry)
            df = df.append(
                {"abs_x": round(x, 3),
                 "abs_y": round(y, 3),
                 "efficiency": getattr(tr_df["efficiency"], aggregate)(),
                 "potential_flux": getattr(tr_df["potential_flux"], aggregate)(),
                 "absorbed_flux": getattr(tr_df["absorbed_flux"], aggregate)(),
                 "cos_factor": getattr(tr_df["cos_factor"], aggregate)(),
                 "shadow_losses": getattr(tr_df["shadow_losses"], aggregate)()
                 }, ignore_index=True)
    geometry = geometry.set_abs_pos(0,0)
    return df

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

def export_obj_vtk(az, zen, receiver = "geometry/receiver.yaml",
                            geometry = "geometry/data.yaml",
                            rays=100,
                            exp_dir="out"):
    utils.mkdir_if_not_exists(exp_dir)
    pairs = f"{az:.1f},{zen:.1f}"
    objpath = os.path.join(exp_dir, pairs + ".obj")
    vtkpath = os.path.join(exp_dir, pairs + ".vtk")
    obj_cmd = f'solstice  -n 1 -g format=obj -t1 -D {pairs} -R {receiver} {geometry}'.split()
    vtk_cmd = f'solstice  -n {rays} -p default -t1 -D {pairs} -R {receiver} {geometry}'.split()
    with open(objpath, 'w') as o:
        run(obj_cmd, stdout=o)
    with open(vtkpath, 'w') as v:
        run(vtk_cmd, stdout=v)
    utils.del_first_line(vtkpath)
    return objpath, vtkpath

def export_heatmap(azzen_pair_list, geometry, heatpath_receiver, rays=1000000):
    """ Set slices in geometry
    Run solstice to export vtk
    save file and return path """
    return "heatmap_vtk_path"


def read(fname):
    columns = {
           "potential_flux": 2,
           "absorbed_flux": 3,
           "cos_factor": 4,
           "shadow_losses": 5,
           "missing_losses": 6,
           # "reflectivity_losses": 7,
           # "absorptivity_losses": 8
           }
    df = pd.read_csv(fname, sep='\s+', names=range(47))
    df_out = df.loc[df[1] == 'Sun', [3]]  # azimuth (transversal plane)
    df_out.columns = ["azimuth"]
    df_out["zenith"] = df.loc[df[1] == 'Sun', [4]]
    df_out["efficiency"] = df.loc[df[0] == 'absorber', [23]].values
    for key in columns.keys():
        df_out[key] = df[0].iloc[df_out.index + \
                                 columns.get(key)].astype('float').values
    return df_out
