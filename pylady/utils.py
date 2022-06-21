from pathlib import Path
import inspect
import json 
from attrs import field
import re


def format_key(key):
    """Remove curly brackets (), transform to lowercase, strip, replace whitespace with underscore.
    """
    key = key.replace("(", "").replace(")", "")
    key = key.lower().strip().replace(" ", "_")
    return key

def split_sections():
    """Parse old_input file and return a nested dict with each section and the keys:values parameters."""
    with open(Path(__file__).parents[1].joinpath('lib/old_input.ml'), 'r') as f:
        default_config = f.readlines()

    sections = {}
    key = "input"
    sections[key] = {}
    for l in default_config:
        match = re.findall("\!\-+([\w\s]+)", l)
        if len(match) != 0:
            key = format_key(match[0])
            sections[key] = {}
        else:
            c = l.split("=")
            if len(c) == 2:
                sections[key][format_key(c[0])] = c[1].strip()
    return sections

def get_default_parameters():
    """Map sections of the old_input.ml file to objects of pylady, and return a nested dict 
    containing {keys:default_values} for each pylady object."""

    default_parameters = {}
    categories = {"database": ["db_and_elements"],
                 "model": ["input", 
                           "function_fit_form",
                           "algo_fit",
                           "kernel",
                           "milady",
                           "genetical_algo",
                           "lbfgs"
                           ],
                 "descriptors": ["descriptors",
                                 "g2",
                                 "g3",
                                 "behpar",
                                 "afs",
                                 "mtp",
                                 "so3",
                                 "so4",
                                 "soap",
                                 "body",
                                 "acd"],
                 "unused": ["old_unused"]}
    old_in_dict = split_sections()
    for pylady_key, old_input_keys in categories.items():
        default_parameters[pylady_key] = {}
        for i in old_input_keys:
            default_parameters[pylady_key].update(old_in_dict[i])
    return default_parameters

def get_defaults_as_fields(category):
    """Pass a dict of {parameter:attrs.field(default=default_value...)} to create pylady objects 
    with the relevant parameters and their default values.
    
    category: either 'database', 'model' or 'descriptors'
    """
    d = {parameter: field(default=value, 
                            metadata={"milady_config":True, "milady_config_type":category}) 
            for parameter, value in get_default_parameters()[category].items()}
    return d