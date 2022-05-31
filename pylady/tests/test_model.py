from distutils.command.build import build
import pylady
import pytest

empty_system = pylady.System("pylady/tests/empty.md")
valid_system = pylady.System("pylady/tests/valid.poscar")


def build_model(system, safety_checks=True):
    c1 = pylady.Collection(name="1",
                    systems=[system], 
                    w_energy=1.0)
    desc = pylady.Descriptor(desc_type=1, r_cut=4)
    d = pylady.Database(collections=[c1])
    m = pylady.Model(database=d, descriptor=desc, ml_type=-1, kw_arguments={"1":1}, safety_checks=safety_checks)
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
