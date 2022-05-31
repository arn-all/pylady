from pathlib import Path

import attrs
from attrs import define, field, validators
from attrs.validators import instance_of
# Note: 
# Classes are written based on the attrs library to avoid boilerplate code.
# Please refer to attrs docs for details.

@define(kw_only=True) # no positional argument
class Descriptor():
    """Base descriptor class.
    """

    desc_type: int = field(validator=validators.instance_of(int))
    r_cut: float = field(validator=validators.instance_of((float, int)))

    def compute(self, systems):
        from pylady.model import Model
        from pylady.database import Database
        from pylady.database import Collection

        db = Database(collections=Collection(name="descriptor_only", 
                                            systems=systems))
        m = Model(database=db, descriptor=self, ml_type=-1)
        m.run()
        return m.database.collections["descriptor_only"].descriptors

    @classmethod
    def G2(cls, r_cut):
        return cls(desc_type=1, r_cut=r_cut)

    @classmethod
    def G3(cls, r_cut):
        return cls(desc_type=2, r_cut=r_cut)

    @classmethod
    def Behler(cls, r_cut):
        return cls(desc_type=3, r_cut=r_cut)

    @classmethod
    def AFS(cls, r_cut):
        return cls(desc_type=4, r_cut=r_cut)
    
    @classmethod
    def SOAP(cls, r_cut):
        return cls(desc_type=5, r_cut=r_cut)

    @classmethod
    def PSO3(cls, r_cut):
        return cls(desc_type=6, r_cut=r_cut)

    @classmethod
    def BSO3(cls, r_cut):
        return cls(desc_type=7, r_cut=r_cut)

    @classmethod
    def PSO4(cls, r_cut):
        return cls(desc_type=8, r_cut=r_cut)
    
    @classmethod
    def BSO4(cls, r_cut):
        return cls(desc_type=9, r_cut=r_cut)

    @classmethod
    def Hybrid_G2_AFS(cls, r_cut):
        return cls(desc_type=14, r_cut=r_cut)

    @classmethod
    def Hybrid_G2_BSO4(cls, r_cut):
        return cls(desc_type=19, r_cut=r_cut)
    
    @classmethod
    def MTP3(cls, r_cut):
        return cls(desc_type=100, r_cut=r_cut)