from ruamel.yaml import YAML
import json

yaml = YAML(typ='safe')

class Spec():
    """
    This is the base class for everything related to loading fragments/specs
    """
    def __init__(self, name, fname):
        self.name = name
        self.data = self._load_specs(fname)
        self.default = self._maybe_load_defaults()


    def __str__(self):
        return json.dumps(self.data, indent=4)

    def print_overview(self):
        print("""
  Available Experiments
""")
        for exp in self.data:
            print("  {}".format(exp['spec']))


    def _load_specs(self, specfile):
        with open(specfile, 'r') as stream:
            data = yaml.load(stream)
            #remove top level name
            datareduced = [i[self.name] for i in data]
            return datareduced

    def _maybe_load_defaults(self):
        for spec in self.data:
            if spec['spec'] == 'default':
                # print('found default!')
                return spec
        return 'none'

    def _findSpec(self, identifier):
        spec = next(
            (item
             for item in self.data if item['spec'] == identifier),
            None)
        if spec is None:
            raise KeyError("spec identifier {} not found".format(identifier))
        else:
            return spec

    def get_spec(self, identifier):
        spec = self._findSpec(identifier)
        if self.default != 'none':
            # preserve spec name
            orig_specname = spec['spec']
            self.default.update(spec)
            spec = self.default
            spec['spec'] = 'default -> ' + orig_specname
        return spec


