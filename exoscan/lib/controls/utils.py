import sys, importlib, os
from pkgutil import walk_packages
from log_conf.logger import logger


def import_all_controls(services: str = None) -> list[tuple]:
    try: 
        controls = []
        modules = []

        modules += fetch_modules()
        
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
    

def fetch_modules():
    
    module_path = f"exoscan.lib.controls"
    # if service: 
    #     module_path += f".{service}"
    return walk_packages(
        importlib.import_module(module_path).__path__,
        importlib.import_module(module_path).__name__ + "."
    )