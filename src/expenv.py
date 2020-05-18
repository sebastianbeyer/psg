import os
from pathlib import Path
import paths


class ExperimentEnvironment():
    """
    The environment (folder) for an experiment
    """
    def __init__(self, exp):
        self.name = exp.spec
        self.path = self._gen_path()
        filename = 'run-{}.sh'.format(self.name)
        self.runfile = os.path.join(self.path, filename)

    def copy_inputfiles(self):
        """Copy the input files into the experiment path
        """

    def _gen_path(self):
        exppath = os.path.join(paths.exp_envs_path, self.name)
        Path(exppath).mkdir(parents=True, exist_ok=True)
        return os.path.join(paths.exp_envs_path, self.name)
