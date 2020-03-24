import os
import jinja2
import paths
from time import asctime
import version


class Experiment():
    """
    Class for a running experiment that can be dumped out as a shell file
    """
    def __init__(self, exp, time, grid, icedyn, ocean, climate):
        self.spec = exp['spec']
        self.exp = exp
        self.time = time
        self.grid = grid
        self.icedyn = icedyn
        self.ocean = ocean
        self.climate = climate
        self.timestamp = asctime()

        self.version = version.git_version()

        output = {
                'base': os.path.join(paths.exp_envs_path, self.spec, self.spec + '.nc', ),
                'ts_file': os.path.join(paths.exp_envs_path, self.spec, 'ts_' + self.spec + '.nc', ),
                'extra_file': os.path.join(paths.exp_envs_path, self.spec, 'ex_' + self.spec + '.nc', ),
                'extra_vars': 'velsurf_mag,mask,thk,topg,usurf,climatic_mass_balance',
                }
        self.basedata = {
                'timestamp': asctime(),
                'psg_revision': self.version,
                'exp_name': self.spec,
                'n_procs': self.exp['n_procs'],
                'netcdfIn': self.exp['netcdf_input'],
                'config_override': self.exp['config_override'],
                'bootstrap': self.exp['bootstrap'],
                'output': output,
                }

    def __str__(self):
        string = """
        Basics:
            Experiment:      {}
            Input Netcdf:    {}
            Bootstrap:       {}
            Config override: {}
            Processors:      {}
            PSG-Version:     {}
        Fragments:
            Grid:        {}
            Icedynamic   {}
            Ocean:       {}
            Climate:     {}
            Time:        {}
        """.format(
                self.spec,
                self.basedata['netcdfIn'],
                self.basedata['bootstrap'],
                self.basedata['config_override'],
                self.basedata['n_procs'],
                self.version,
                self.grid['spec'],
                self.icedyn['spec'],
                self.ocean['spec'],
                self.climate['spec'],
                self.time['spec'],
                )
        return string

    def write_to_file(self, out_file, templateName):
        loader = jinja2.FileSystemLoader(searchpath=paths.templates_path)
        env = jinja2.Environment(loader=loader,
                                 trim_blocks=True,
                                 undefined=jinja2.StrictUndefined)

        template = env.get_template(templateName)
        template.stream(self.basedata).dump(out_file)

        self._append_options(out_file)

    def _append_options(self, out_file):
        """
        Write each separately
        """
        print('Writing runfile to {}'.format(out_file))
        with open(out_file, 'a') as f:
            for submodel in [self.grid, self.time, self.icedyn, self.ocean, self.climate]:
                for key, value in submodel.items():
                    if key != 'spec':
                        line = "-{} {} \\".format(key, value)
                        # print(line)
                        f.write('  ' + line + '\n')
