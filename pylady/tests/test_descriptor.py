import pylady
import pytest


def test_descriptor_compute():
    d = pylady.Descriptor(desc_type=1, r_cut=2)
    d.compute(["pylady/tests/valid.poscar"])