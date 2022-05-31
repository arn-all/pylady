from distutils.command.build import build
import pylady
import pytest

def build_model(file, safety_checks=True):
    c1 = pylady.Collection(name="1",
                    systems=[file], 
                    w_energy=1.0)
    desc = pylady.Descriptor(desc_type=1, r_cut=4)
    d = pylady.Database(collections=[c1])
    m = pylady.Model(database=d, descriptor=desc, ml_type=-1, kw_arguments={"1":1}, safety_checks=safety_checks)
    return m

def test_fit_model():
    """Typical usecase of the class"""
    m = build_model("pylady/tests/valid.poscar")
    m.fit()

def test_fit_model_empty_file():
    m = build_model("pylady/tests/empty.md")
    with pytest.raises(RuntimeError):
        m.fit()

def test_fit_model_ignore_empty_file():
    m = build_model("pylady/tests/empty.md", safety_checks=False)
    m.fit()