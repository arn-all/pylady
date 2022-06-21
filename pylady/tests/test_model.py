import pylady
import pytest, inspect
from pathlib import Path

tests_dir = Path(inspect.getfile(pylady)).parent.joinpath("tests")

empty_system = pylady.System(str(tests_dir.joinpath("empty.md")))
valid_system = pylady.System(str(tests_dir.joinpath("valid.poscar")))

def build_model(system, safety_checks=True, start_train_from_system_n=0):
    c1 = pylady.Collection(name="1",
                    systems=[system], 
                    w_energy=1.0,
                    start_train_from_system_n=start_train_from_system_n)
    desc = pylady.Descriptor(desc_type=1, r_cut=4)
    d = pylady.Database(collections=[c1])
    m = pylady.Model(database=d, descriptor=desc, ml_type=-1, safety_checks=safety_checks)
    return m


def test_fit_model():
    """Typical usecase of the class"""
    m = build_model(valid_system)
    m.fit()

def test_fit_model_empty_file():
    m = build_model(empty_system)
    with pytest.raises(RuntimeError):
        m.fit()

def test_fit_model_ignore_empty_file():
    m = build_model(empty_system, safety_checks=False)
    m.fit()

def test_fit_request_train_too_many_systems():
    m = build_model(valid_system, start_train_from_system_n=1)

test_fit_model()