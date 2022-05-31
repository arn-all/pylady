
from multiprocessing.sharedctypes import Value
import pylady
import pytest


## Collection

def test_create_collection():
    """Typical usecase of Collection class"""
    c1 = pylady.Collection(name="1",
                    systems=['pylady/tests/empty.md'], 
                    w_energy=1.0, w_force=1.0, w_stress=1.0)

def test_create_collection_missing_file():
    with pytest.raises(AssertionError):
        c1 = pylady.Collection(name="1",
                        systems=['pylady/tests/non_existing_file.foo'], 
                        w_energy=1.0)


## Database 

def test_create_db():
    """Typical usecase of Database class"""

    c1 = pylady.Collection(name="1",
                    systems=['pylady/tests/empty.md'], 
                    w_energy=1.0)
    c2 = pylady.Collection(name="2",
                systems=['pylady/tests/empty.md'], 
                w_energy=2.0)

    d = pylady.Database(collections=[c1, c2])

def test_create_db_same_name():
    """Two collections with the same nametag"""
    c1 = pylady.Collection(name="1",
                    systems=['pylady/tests/empty.md'], 
                    w_energy=1.0)
    c2 = pylady.Collection(name="1",
                systems=['pylady/tests/empty.md'], 
                w_energy=2.0)
    with pytest.raises(ValueError):
        d = pylady.Database(collections=[c1, c2])

def test_create_db_same_collection():
    """Two collections with different names but the same content."""
    c1 = pylady.Collection(name="1",
                    systems=['pylady/tests/empty.md'], 
                    w_energy=1.0)
    c2 = pylady.Collection(name="1",
                systems=['pylady/tests/empty.md'], 
                w_energy=1.0)
    
    with pytest.raises(ValueError):
        d = pylady.Database(collections=[c1, c2])

