import sys, importlib
from typing import Any, get_type_hints, Union
from dataclasses import is_dataclass
from pkgutil import walk_packages
from log_conf.logger import logger


#looks for paths with controls in them in exoscan.lib.controls and returns them to calling function as list
def import_all_controls(services: str = None) -> list[tuple]:
    try: 
        controls = []
        modules = []

        module_path = f"exoscan.lib.controls"
        modules = walk_packages(
        importlib.import_module(module_path).__path__,
        importlib.import_module(module_path).__name__ + "."
        )
        
        for module_name in modules:
            control_module_name = module_name.name

            if (control_module_name.count(".") == 6):
                control_path = module_name.module_finder.path
                control_name = control_module_name.split(".")[-1]
                control_info = (control_name, control_path)
                controls.append(control_info)

    except Exception as e:
        logger.critical(f"{e.__class__.__name__}[{e.__traceback__.tb_lineno}]: {e}")
        sys.exit(1)
    else:
        return controls
    

def parse_response(cls, data: Any):
    if isinstance(data, list):
        return[parse_response(cls.__args__[0], item) for item in data]
    if is_dataclass(cls):
        fieldtypes = get_type_hints(cls)
        return cls(**{
            field: parse_response(fieldtypes[field], data[field])
            for field in data if field in fieldtypes
    })
    return data
        
