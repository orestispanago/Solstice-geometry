import yaml
from dicts_to_yaml import yaml_items
from subprocess import PIPE, Popen
from io import StringIO
import pandas as pd


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()

def format_yaml():
    return yaml.dump(yaml_items, Dumper=MyDumper,default_flow_style=None,
              sort_keys=False)



def run_solstice_df():
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(input=a.encode())
    b = StringIO(out.decode())
    return read(b)

def run_solstice():
    with open("out.txt", "w") as f:
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(input=a.encode())
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
    df_out["efficiency"] = df.loc[df[0] == 'absorber', [23]].values
    for key in columns.keys():
        df_out[key] = df[0].iloc[df_out.index + \
                                 columns.get(key)].astype('float').values
    return df_out

a = format_yaml()
cmd = ['solstice', '-D', '45.0,0', '-n', '100', '-v', 
       '-R', 'geometry/receiver.yaml']

df = run_solstice_df(a)
# run_solstice()