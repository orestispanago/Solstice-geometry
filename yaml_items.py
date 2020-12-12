import yaml


class YamlItems:
    def __init__(self, items=[]):
        self.items = [i.to_dict() for i in items]
        pass

    def add(self, other):
        self.items.append(other.to_dict())

    def write_yaml(self, fpath):
        with open(fpath, 'w') as outfile:
            yaml.dump(self.items, outfile, Dumper=MyDumper,
                      default_flow_style=None, sort_keys=False)


class MyDumper(yaml.SafeDumper):
    # HACK: insert blank lines between top-level objects
    # inspired by https://stackoverflow.com/a/44284819/3786245
    def write_line_break(self, data=None):
        super().write_line_break(data)
        if len(self.indents) == 1:
            super().write_line_break()
