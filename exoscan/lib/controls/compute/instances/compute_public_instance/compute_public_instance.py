from exoscan.lib.controls.compute.instances.inventory import get_instances
from exoscan.lib.controls.models import Instance, InstanceContainer

def execute_logic():
    all_instances = get_instances()
    print(all_instances.instances[1].name)
    return
