import attrs
from attrs import define, field, validators


@define
class BaseClass():


    def as_dict(self):
        return attrs.asdict(self)

    def get_config(self):
    
        d = {}
        for i in self.__attrs_attrs__:
            if "milady_config" in i.metadata:
                d[i.name] = str(self.as_dict()[i.name]).lstrip()
        return d