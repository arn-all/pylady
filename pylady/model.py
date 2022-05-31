from pathlib import Path
import subprocess


from pylady.database import Database
from pylady.descriptors import Descriptor

import attrs
from attrs import define, field, validators
from attrs.validators import instance_of
# Note: 
# Classes are written based on the attrs library to avoid boilerplate code.
# Please refer to attrs docs for details.

@define(kw_only=True) # no positional argument
class Model():
    """The ML model class, which associates hyperparameters and a database.

    Parameters
    ----------

    ml_type: int
        Description


    """

    ml_type: int = field(validator=validators.instance_of(int))
    descriptor: Descriptor = field(validator=validators.instance_of(Descriptor))
    database: Database = field(validator=validators.instance_of(Database))
    safety_checks: bool = field(default=True, validator=validators.instance_of(bool))
    kw_arguments: dict = field(factory=dict)

    def __attrs_post_init__(self):
        self.kw_arguments = self.get_arguments()

    def fit(self, n_jobs=1, directory=None):
        """Prepare the run, fit the Milady model and retrieve data.
        """
        self.pre_run(directory)
        self.run(n_jobs)
        self.post_run(directory)

    def get_arguments(self):
        """Get arguments that will be passed to Milady
        """
        # mix self.kw_arguments and self.descriptor / database / model kw values
        pass

    def pre_run(self, directory):
        """Prepare run.
        Populate the directory where Milady will be run. 
        Check for any issue with input data if safety_checks are activated."""

        if self.safety_checks:
            self.database.check_entries_format()
            self.database.check_duplicate_systems()

        self.populate_run_directory(directory)

    def run(self, n_jobs=1):
        """Run the Milady Fortran code externally on n_jobs parallel mpi processes."""
        # status = subprocess.run()
        # return status
        pass

    def post_run(self, directory):
        """Post run step. Time to explore results !"""
        self.parse_log()
        self.parse_descriptors()

    def as_dict(self):
        return attrs.asdict(self)

    def populate_run_directory(self, directory):
        """Create the directory if not existent, copy files necessary for milady run.
        """
        self.fill_ml_file()

    def fill_ml_file(self):
        """Prepare milady configuration file by template filling.
        """
        pass

    def parse_log(self):
        """"Parse Milady logs after runtime."""
        # Check for errors
        # Save logs to Model.log
        pass

    def parse_descriptors(self):
        """Load descriptors files as numpy arrays."""
        # Load descriptors files in numpy nd_array
        # 1st column IS NOT an index