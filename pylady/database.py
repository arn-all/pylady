from pathlib import Path

import attrs
from attrs import define, field, validators
from attrs.validators import instance_of

import ase.io.vasp
import hashlib
import numpy as np

from pylady.descriptors import Descriptor

# Note: 
# Classes are written based on the attrs library to avoid boilerplate code.
# Please refer to attrs docs for details.

def check_fitting_weights(instance, attribute, value):
    if not isinstance(value, float):
        if (len(value)!=2) or (not isinstance(value[0], (int, float))) or (not isinstance(value[1], (int, float))):
            raise ValueError(f"Incorrect value or type for {attribute.name}, got: {value}")

def contains(collect, collections):
        return any([collect==d for d in collections.values()])

def file_fingerprint(file_name):
    with open(file_name, 'r') as f:
        return hashlib.sha1(f.read().encode()).hexdigest()


@define()
class System():
    """A collection of atomic systems, which share the same ML fitting hyperparameters.
    """

    # name is ignored when checking equality
    poscar: str = field(validator=validators.instance_of(str))
    weight_per_element: list = field(factory=list, kw_only=True)

    def check_readable(self):
        ase.io.vasp.read_vasp(self.poscar)

@define(kw_only=True) # no positional argument
class Collection():
    """A collection of atomic systems, which share the same ML fitting hyperparameters.
    """

    # name is ignored when checking equality
    name: str = field(validator=validators.instance_of(str), eq=False)
    index: int = field(default=0)
    w_energy: float or 'list[float]' = field(default=0.0, validator=check_fitting_weights)
    w_force:  float or 'list[float]' = field(default=0.0, validator=check_fitting_weights)
    w_stress: float or 'list[float]' = field(default=0.0, validator=check_fitting_weights)

    systems: list = field(factory=list, 
                            validator=validators.instance_of(list))
    
    descriptors: 'list[np.array]' = field(factory=list)

    @systems.validator
    def files_exist(self, attribute, value):
        assert len(value) > 0, "Empty list of systems"
        for f in value:
            # Check for file existence.
            # Format correctness will be checked at read-time
            assert Path(f.poscar).is_file(), f"Non existing file: {f}"

    test_size: float = field(default=0.0, validator=validators.instance_of(float))
    start_train_from_system_n: int = field(default=0)

    @test_size.validator
    def check_below_1(self, attribute, value):
        assert 0 <= value <= 1, f"Testing set size must be a float between 0 and 1, got: {value}"

    n_train_systems: int = field(default=None)

    fingerprints: list = field(factory=list)
    
    def __attrs_post_init__(self):
        for s in self.systems:
            self.fingerprints.append(file_fingerprint(s.poscar))
        if self.n_train_systems is None:
            self.n_train_systems = round((len(self.systems)-self.start_train_from_system_n)*(1-self.test_size))
        assert self.start_train_from_system_n + self.n_train_systems <= len(self.systems), "Number of systems to use for train + number of the first configuration to use exceeds the total number of systems."

    def check_systems_are_readable(self):
        """Open vasp files to check they are ase-readable.
        Milady also requires the first line to follow a special format, which is not checked yet.
        """
        for system in self.systems:
            try:
                system.check_readable()
            except:
                raise RuntimeError(f"Error while reading file {system.poscar} due to format or access issue.\n")

@define(kw_only=True)
class Database():
    """A database of all the different collections to use in a Model.
    Databases can be saved/loaded in JSON format for easy share and reuse.
    """

    collections = field(factory=list)

    def __attrs_post_init__(self):
        if isinstance(self.collections, Collection):
            self.collections = [self.collections]

        collect_dict = {}
        for i, c in enumerate(self.collections):
            c.index = i
            if contains(c, collect_dict):
                raise ValueError(f"A collection with the same content already exists (ignoring the name attribute):\n{c}")
            elif any([c.name == n for n in collect_dict.keys()]):
                raise ValueError(f"A collection with the name '{c.name}' already exists")
            else:
                collect_dict[c.name] = c
        self.collections = collect_dict

    def get_arguments(self):
        return {}

    def add(self, collection):
        if contains(collection, self.collections):
            raise ValueError(f"Provided collection is already present in database (ignoring the name attribute):\n{collection}")
        self.collections[collection.name] = collection

    def remove(self, name):
        del self.collections[name]
    
    def clear_collections(self):
        self.collections = {}

    def as_dict(self):
        return attrs.asdict(self)

    def as_df(self):
        import pandas as pd
        return pd.DataFrame.from_dict(self.as_dict()["collections"], 
                                        orient="index")

    def get_global_number_systems(self):
        n = 0
        for c in self.collections.values():
            n += len(c.systems)
        return n
    
    def check_entries_format(self):
        for c in self.collections.values():
            c.check_systems_are_readable()

    def check_duplicate_systems(self):
        hashes = []
        for c in self.collections.values():
            hashes += c.fingerprints
        return len(hashes) == len(set(hashes))