import os
import numpy as np
import subprocess
import utils
from io import StringIO
import pandas as pd
from tqdm import tqdm

CWD = os.getcwd()
receiver = os.path.join(CWD, "geometry", "receiver.yaml")


class Trace():

    def __init__(self, min_angle, max_angle, step, rays, geometry, name):
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.step = step
        self.rays = rays
        self.angles = np.arange(min_angle, max_angle + 1, step).tolist()
        self.name = name
        self.title = self.name + " " + geometry.split(".")[0]
        self.geometry_path = os.path.join(CWD, "geometry", geometry)
        self.exp_dir = os.path.join(CWD, 'export', geometry.split(".")[0])
        self.shape_dir = os.path.join(self.exp_dir, "shapes")
        self.rawfile = os.path.join(self.exp_dir, 'raw', self.name + ".txt")
        self.df = None

    def run(self):
        utils.mkdir_if_not_exists(os.path.dirname(self.rawfile))
        with open(self.rawfile, 'w') as f:
            # Solstice cannot take too long string of angle arguments, so split into chunks
            for i in range(0, len(self.angle_pairs), 50):
                chunk = self.angle_pairs[i:i + 50]
                chunk = ":".join(chunk)
                cmd = f'solstice -D {chunk} -n {self.rays} -v -R {receiver} {self.geometry_path}'.split()
                subprocess.run(cmd, stdout=f)

    def run_to_df(self):
        """ Runs Direction and pipes output to dataframe """
        df_list = []
        # Solstice cannot take too long string of angle arguments, so split into chunks
        for i in tqdm(range(0, len(self.angle_pairs), 20)):
            chunk = self.angle_pairs[i:i + 20]
            chunk = ":".join(chunk)
            cmd = f'solstice -D {chunk} -n {self.rays} -v -R {receiver} {self.geometry_path}'.split()
            a = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            b = StringIO(a.communicate()[0].decode('utf-8'))
            df = read(b)
            df_list.append(df)
        return pd.concat(df_list)

    def export_vtk(self, nrays=100):
        for pair in [self.angle_pairs[0], self.angle_pairs[-1]]:
            pair_str = pair.replace(',', '_')
            fname = f"{self.name}_{pair_str}.vtk"
            utils.mkdir_if_not_exists(self.shape_dir)
            vtkpath = os.path.join(self.exp_dir, "shapes", fname)
            cmd = f'solstice  -n {nrays} -p default -t1 -D {pair} -R {receiver} {self.geometry_path}'.split()
            with open(vtkpath, 'w') as f:
                subprocess.run(cmd, stdout=f)
            utils.del_first_line(vtkpath)

    def export_objs(self):
        """ Export first and last angle_pairs objects """
        for pair in [self.angle_pairs[0], self.angle_pairs[-1]]:
            pair_str = pair.replace(',', '_')
            fname = f"{self.name}_{pair_str}.obj"
            utils.mkdir_if_not_exists(self.shape_dir)
            objpath = os.path.join(self.shape_dir, fname)
            cmd = f'solstice  -n 100 -g format=obj -t1 -D {pair} -R {receiver} {self.geometry_path}'.split()
            with open(objpath, 'w') as f:
                subprocess.run(cmd, stdout=f)

    def export_heat(self, nrays=1000000):
        receiver_heat = os.path.join(CWD, "geometry", "heatmap", "receiver.yaml")
        geometry_heat = os.path.join(CWD, "geometry", "heatmap", "geometry.yaml")
        for pair in [self.angle_pairs[0], self.angle_pairs[-1]]:
            pair_str = pair.replace(',', '_')
            fname = f"{self.name}_{pair_str}_heatmap.vtk"
            heat_path = os.path.join(self.exp_dir, "shapes", fname)
            cmd = f'solstice  -n {nrays} -v -t16 -D {pair} -R {receiver_heat} {geometry_heat}'.split()
            with open(heat_path, 'w') as f:
                subprocess.run(cmd, stdout=f)
            utils.del_until(heat_path)


class Transversal(Trace):
    def __init__(self, min_angle, max_angle, step, rays, geometry):
        super().__init__(min_angle, max_angle, step, rays, geometry, name=self.__class__.__name__)
        self.angle_pairs = [f"{a:.1f},0" for a in self.angles]
        self.sun_col = 3  # sun direction column in txt output file


class Longitudinal(Trace):
    def __init__(self, min_angle, max_angle, step, rays, geometry):
        super().__init__(min_angle, max_angle, step, rays, geometry, name=self.__class__.__name__)
        self.angle_pairs = [f"180,{a:.1f}" for a in self.angles]
        self.sun_col = 4  # sun direction column in txt output file


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
    df_out = df.loc[df[1] == 'Sun', [3]]  # azimuth
    df_out.columns = ["azimuth"]
    df_out["zenith"] = df.loc[df[1] == 'Sun', [4]]  # zenith
    df_out["efficiency"] = df.loc[df[0] == 'entity_all.absorber', [23]].values  # Overall effficiency, add [23,24] for error
    for key in columns.keys():
        df_out[key] = df[0].iloc[df_out.index + columns.get(key)].astype('float').values
    return df_out
