from pathlib import Path
import subprocess
import tempfile
from jinja2 import Environment, FileSystemLoader, StrictUndefined
import inspect

from traitlets import default 
import pylady
import numpy as np
import logging, uuid

from pylady.database import Database
from pylady.descriptors import Descriptor
from pylady.baseclass import BaseClass
import pylady.utils

import attrs
from attrs import define, field, validators
from attrs.validators import instance_of
# Note: 
# Classes are written based on the attrs library to avoid boilerplate code.
# Please refer to attrs docs for details.

import json
from os.path import expanduser

def load_global_config():
    config_file = expanduser("~/.config/milady_config.json")
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    except json.decoder.JSONDecodeError:
        raise RuntimeError(f"Missing configuration file at {config_file}. Run `pylady setup` in a terminal.")

MILADY_CONFIG = load_global_config()


@define(kw_only=True)
class BaseModel(BaseClass):
    """The ML model class, which associates hyperparameters and a database.

    Parameters
    ----------

    ml_type: int
        Description


    """

    name: str = field(default='', validator=validators.instance_of(str))
    ml_type: int = field(validator=validators.instance_of(int))
    descriptor: Descriptor = field(validator=validators.instance_of(Descriptor))
    database: Database = field(validator=validators.instance_of(Database))
    safety_checks: bool = field(default=True, validator=validators.instance_of(bool))
    design_matrix: np.ndarray = field(default=None)

    def fit(self, n_jobs=1, save_directory="milady_results", debug=False, **kwargs):
        """Prepare the run, fit the Milady model and retrieve data.
        """
        unique_id = str(uuid.uuid4()).split("-")[0]

        # create folder for writing ouput
        save_directory = Path(save_directory).joinpath(unique_id)
        save_directory.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(filename=Path(save_directory).joinpath('milady.log'), 
                            encoding='utf-8', 
                            level=logging.DEBUG if debug else logging.WARNING)
    
        # run milady in a tempdir
        with tempfile.TemporaryDirectory() as tmpdirname:
            self.pre_run(run_directory=tmpdirname)

            completed = self.run(n_jobs, 
                                run_directory=tmpdirname)

            self.post_run(run_directory=tmpdirname, 
                          completed_process=completed, 
                          output_directory=save_directory)

    # def get_arguments(self):
    #     """Get arguments that will be passed to Milady.
    #     Mixes user-specified self.kw_arguments, self.descriptor / database args and default kw values
    #     """
    #     args = pylady.utils.get_default_as_dict()
    #     args["descriptors"].update(self.descriptor.get_arguments())
    #     args["database"].update(self.database.get_arguments())
    #     args["model"].update(self.kw_arguments)

    #     for user_arguments in [self.descriptor.get_arguments(),
    #                            self.database.get_arguments(),
    #                            self.kw_arguments]:
    #         args.update(user_arguments)

    def pre_run(self, run_directory):
        """Prepare run.
        Populate the directory where Milady will be run. 
        Check for any issue with input data if safety_checks are activated."""

        if self.safety_checks:
            self.database.check_entries_format()
            self.database.check_duplicate_systems()

        self.populate_run_directory(run_directory)

    def run(self, n_jobs, run_directory):
        """Run the Milady Fortran code externally on n_jobs parallel mpi processes."""
        
        set_env_cmd = MILADY_CONFIG["set_env_cmd"]
        run_milady_cmd = MILADY_CONFIG["run_milady_cmd"].format(n_jobs=n_jobs)
        
        status = subprocess.run(set_env_cmd + " && " + run_milady_cmd, 
                                shell=True,
                                cwd=run_directory,
                                capture_output=True)
        
        logging.info(status.stdout.decode())
        return status

    def post_run(self, run_directory, completed_process, output_directory):
        """Post run step. Time to explore results !
        Create a directory with unique ID model-name_model-sha in save_directory and store results there.
        OR use HDF5 container !?"""

        with open(Path(output_directory).joinpath("stdout.log"), "w") as f:
            f.write(completed_process.stdout.decode())

        with open(Path(output_directory).joinpath("stderr.log"), "w") as f:
            f.write(completed_process.stdout.decode())

        self.parse_log()
        self.parse_descriptors()

    def populate_run_directory(self, directory):
        """Copy files necessary for milady run.
        """
        def save_to_tmp_dir(name, content):
            with open(Path(directory).joinpath(name), "w") as f:
                f.write(content)

        to_write = {"db_model.in": self.fill_template_file("db_model_in.txt"),
                    "name.in": "config",
                    "config.ml": self.fill_template_file("config_ml.txt"),
                    "eamtab.potin": self.fill_template_file("eamtab.potin"),
                    "config.din": self.fill_template_file("config.din"),
                    "config.gin": self.fill_template_file("config.gin")}
        
        for name, contents in to_write.items():
            save_to_tmp_dir(name, contents)

    def fill_template_file(self, file):
        """Prepare milady configuration file by template filling.
        """
        # location of templates
        template_dir = Path(inspect.getfile(pylady)).parents[1].joinpath('templates')
        
        env = Environment(loader=FileSystemLoader(template_dir))
        
        template = env.get_template(file)
        return template.render(model=self, defaults=pylady.utils.get_default_as_dict())

    def parse_log(self):
        """"Parse Milady logs after runtime."""
        # Check for errors
        # Save logs to Model.log
        pass

    def parse_descriptors(self):
        """Load descriptors files as numpy arrays."""
        # Load descriptors files in numpy nd_array
        # 1st column IS NOT an index
        pass

Model = attrs.make_class('Model', 
                        pylady.utils.get_defaults_as_fields("model")["model"], 
                        bases=(BaseModel,))