from ruamel.yaml import YAML

yaml = YAML(typ='safe')


class Spec():
    """
    This is the base class for everything related to loading fragments/specs
    """
    def __init__(self, name, fname):
        self.name = name
        self.data = self._load_specs(fname)

    def _load_specs(self, specfile):
        with open(specfile, 'r') as stream:
            return yaml.load(stream)

    def findSpec(self, identifier):
        spec = next(
            (item[self.name]
             for item in self.data if item[self.name]['spec'] == identifier),
            None)
        if spec is None:
            raise KeyError("spec identifier {} not found".format(identifier))
        else:
            return spec
