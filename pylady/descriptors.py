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