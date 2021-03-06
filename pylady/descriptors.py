from pathlib import Path
from pylady.baseclass import BaseClass

import attrs
from attrs import define, field, validators
from attrs.validators import instance_of
# Note: 
# Classes are written based on the attrs library to avoid boilerplate code.
# Please refer to attrs docs for details.

DEFAULTS = {"r_cut": 5.0}

@define(kw_only=True) # no positional argument
class Descriptor(BaseClass):
    """Base descriptor class.
    """

    desc_type: int = field(validator=validators.instance_of(int))
    r_cut: float = field(default=DEFAULTS["r_cut"],
                         validator=validators.instance_of((float, int)))
    n_g2_eta : float = field(default=0.0)
    eta_max_g2 : float = field(default=0.0)

    def compute(self, systems):
        from pylady.database import Collection
        from pylady.database import Database
        from pylady.model import Model

        db = Database(collections=Collection(name="descriptor_only", 
                                            systems=systems))
        m = Model(database=db, descriptor=self, ml_type=-1)
        m.fit()
        return m.database.collections["descriptor_only"].descriptors

    @classmethod
    def G2(cls, r_cut=DEFAULTS["r_cut"], n_g2_eta=None, eta_max_g2=None):
        return cls(desc_type=1, r_cut=r_cut, n_g2_eta=n_g2_eta, eta_max_g2=eta_max_g2)

    @classmethod
    def G3(cls, r_cut=DEFAULTS["r_cut"]):
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