import jinja2
import paths
from time import asctime


class Experiment():
    """
    Class for a running experiment that can be dumped out as a shell file
    """
    def __init__(self, exp, time, grid, icedyn):
        self.spec = exp['spec']
        self.exp = exp
        self.time = time
        self.grid = grid
        self.icedyn = icedyn
        self.timestamp = asctime()

        setup = {
            'do_atmGiven': False,
            'do_pdd': True,
            'do_glacialIndex': True,
            'do_bootstrap': True,
            'do_sealevel': True,
        }

        ocean = {
            'sealevelFile': 'delta_sl.nc',
        }

        self.exp_data = {
            'exp_name': self.spec,
            'timestamp': asctime(),
            'netcdfIn': "./input.nc",
            'n_procs': 5,
            'config_override': "./config.nc",
            'setup': setup,
            'grid': grid,
            'time': time,
            'iceDynamics': icedyn,
            'ocean': ocean,
        }

    def write_to_file(self, out_file, templateName):
        loader = jinja2.FileSystemLoader(searchpath=paths.templates_path)
        env = jinja2.Environment(loader=loader,
                                 trim_blocks=True,
                                 undefined=jinja2.StrictUndefined)

        template = env.get_template(templateName)
        template.stream(self.exp_data).dump(out_file)

    def alternateWrite(self, out_file):
        """
        Write each separately
        """
        for key, value in self.grid.items():
            if key != 'spec':
                line = "-{} {} \\".format(key, value)
                print(line)
