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

a = format_yaml()
cmd = ['solstice', '-D', '45.0,0', '-n', '100', '-v', 
       '-R', 'geometry/receiver.yaml']


def run_solstice_df():
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = p.communicate(input=a.encode())
    b = StringIO(out.decode())
    return pd.read_csv(b, sep='\s+',names=range(47))

def run_solstice():
    with open("out.txt", "w") as f:
        p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate(input=a.encode())
        f.write(out.decode())

df = run_solstice_df()
run_solstice()