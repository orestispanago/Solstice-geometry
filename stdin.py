from geometries import BaseGeometry
from subprocess import PIPE, Popen
from io import StringIO
import pandas as pd
import io

def run_solstice_df(geometry):
    # if geometry.endswith(".yaml"):
    #     cmd.append(geometry)
    #     print("appended")
    with open(geometry, 'r') as f:
        dni = 2000
        newline = f"- sun: {{ dni : {dni} }}\n"
        lines = f.readlines()
        lines[0] = newline
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(input="".join(lines).encode())
        print(err)
        b = StringIO(out.decode())
        print(read(b))

def run_solstice(geometry):
    with open("out.txt", "w") as f:
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(input=geometry.encode())
        f.write(out.decode())

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
    df_out["efficiency"] = df.loc[df[0] == 'base.absorber', [23]].values
    for key in columns.keys():
        df_out[key] = df[0].iloc[df_out.index + \
                                 columns.get(key)].astype('float').values
    return df_out

# a = format_yaml()
cmd = ['solstice', '-D', '45.0,0', '-n', '100', '-v', 
       '-R', 'geometry/receiver.yaml']

bg = BaseGeometry().yaml()
run_solstice_df("geometry/data1.yaml")
# run_solstice()


    