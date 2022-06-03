import pylady
import pytest
import inspect
from pathlib import Path 

tests_dir = Path(inspect.getfile(pylady)).parent.joinpath("tests")
systems = [pylady.System(str(tests_dir.joinpath("valid.poscar")))]
args_values = [int(2), 2.5]

@pytest.mark.parametrize("r", args_values)
def test_descriptor_compute(r):
    d = pylady.Descriptor(desc_type=1, r_cut=r)
    d.compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_G2(r):
    pylady.Descriptor.G2(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_G3(r):
    pylady.Descriptor.G3(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_Behler(r):
    pylady.Descriptor.Behler(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_AFS(r):
    pylady.Descriptor.AFS(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_SOAP(r):
    pylady.Descriptor.SOAP(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_PSO3(r):
    pylady.Descriptor.PSO3(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_BSO3(r):
    pylady.Descriptor.BSO3(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_PSO4(r):
    pylady.Descriptor.PSO4(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_BSO4(r):
    pylady.Descriptor.BSO4(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_Hybrid_G2_AFS(r):
    pylady.Descriptor.Hybrid_G2_AFS(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_Hybrid_G2_BSO4(r):
    pylady.Descriptor.Hybrid_G2_BSO4(r_cut=r).compute(systems)

@pytest.mark.parametrize("r", args_values)
def test_compute_MTP3(r):
    pylady.Descriptor.MTP3(r_cut=r).compute(systems)