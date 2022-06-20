from pathlib import Path
import inspect
import json 
from attrs import field


def default_json_from_old_input():
    
    with open(Path(__file__).parents[1].joinpath('lib/old_input.ml'), 'r') as f:
        default_config = f.readlines()

    param = {}
    for l in default_config:
        c = l.split("=")
        if len(c) == 2:
            param[c[0]] = c[1].strip()
    
    with open(Path(__file__).parents[1].joinpath('lib/docs_options.json'), 'w') as f:
        json.dump(param, f, indent=2)



# def get_docs_contents():
#     ## Read from Json
#     docs_contents_json = Path(__file__).parents[1].joinpath('lib/docs_options.json')
#     with open(docs_contents_json, "r") as f:
#         docs_contents = json.load(f)
#     return docs_contents

# def get_defaults_as_fields(config_type):
#     defaults = {}
#     for entry, values in get_docs_contents().items():
#         defaults[entry] = {k: field(default=v['value'], 
#                             metadata={"milady_config":True, "milady_config_type":config_type}) for k, v in values.items()}
#     return defaults

# def get_default_as_dict():
#     defaults = {}
#     for entry, values in get_docs_contents().items():
#         defaults[entry] = {k: v['value'] for k, v in values.items()}
#     return defaults