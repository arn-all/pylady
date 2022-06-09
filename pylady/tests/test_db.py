

import pylady
import pytest
import pytest, inspect
from pathlib import Path

tests_dir = Path(inspect.getfile(pylady)).parent.joinpath("tests")
empty_system = pylady.System(str(tests_dir.joinpath('empty.md')))
valid_system = pylady.System(str(tests_dir.joinpath('valid.poscar')))

## Collection

def test_create_collection():
    """Typical usecase of Collection class"""
    c1 = pylady.Collection(name="1",
                    systems=[empty_system], 
                    w_energy=1.0, w_force=1.0, w_stress=1.0)

def test_create_collection_missing_file():
    with pytest.raises(AssertionError):
        c1 = pylady.Collection(name="1",
                        systems=[pylady.System(str(tests_dir.joinpath('non_existing_file.foo')))], 
                        w_energy=1.0)


def test_check_readable_success(): 
    pylady.Collection.check_systems_are_readable(
            pylady.Collection(name="1", systems=[valid_system]))

def test_check_readable_fail():
    with pytest.raises(RuntimeError):
        pylady.Collection.check_systems_are_readable(
                pylady.Collection(name="1", systems=[empty_system]))

def test_weight_dict():
    c1 = pylady.Collection(name="1",
                systems=[empty_system], 
                w_energy=1.0,
                w_stress=[0, 2])
    # impose energy weight
    assert c1.weight_params["energy"]["fit"] == "T"
    assert c1.weight_params["energy"]["optimize_w"] == False
    assert c1.weight_params["energy"]["weight_min"] == 1.0
    assert c1.weight_params["energy"]["weight_max"] == 1.0
    

    # do not fit force
    assert c1.weight_params["force"]["fit"] == "F"
    assert c1.weight_params["force"]["optimize_w"] == False
    assert c1.weight_params["force"]["weight_min"] == 0.0
    assert c1.weight_params["force"]["weight_max"] == 0.0
    

    # optimize stress weight in a range
    assert c1.weight_params["stress"]["fit"] == "T"
    assert c1.weight_params["stress"]["optimize_w"] == True
    assert c1.weight_params["stress"]["weight_min"] == 0
    assert c1.weight_params["stress"]["weight_max"] == 2


## Database 

def test_create_db():
    """Typical usecase of Database class"""

    c1 = pylady.Collection(name="1",
                    systems=[empty_system], 
                    w_energy=1.0)
    c2 = pylady.Collection(name="2",
                systems=[empty_system], 
                w_energy=2.0)

    d = pylady.Database(collections=[c1, c2])

def test_create_db_incrementally():
    """Typical usecase of Database class"""

    c1 = pylady.Collection(name="1",
                    systems=[empty_system], 
                    w_energy=1.0)
    c2 = pylady.Collection(name="2",
                systems=[empty_system], 
                w_energy=2.0)

    d = pylady.Database()
    d.add(c1)
    d.add(c2)

def test_create_db_same_name():
    """Two collections with the same nametag"""
    c1 = pylady.Collection(name="1",
                    systems=[empty_system], 
                    w_energy=1.0)
    c2 = pylady.Collection(name="1",
                systems=[empty_system], 
                w_energy=2.0)
    with pytest.raises(ValueError):
        d = pylady.Database(collections=[c1, c2])

def test_create_db_same_collection():
    """Two collections with different names but the same content."""
    c1 = pylady.Collection(name="1",
                    systems=[empty_system], 
                    w_energy=1.0)
    c2 = pylady.Collection(name="1",
                systems=[empty_system], 
                w_energy=1.0)
    
    with pytest.raises(ValueError):
        d = pylady.Database(collections=[c1, c2])
