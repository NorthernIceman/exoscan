import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import Instance, InstanceContainer
from provider.return_regions import return_regions
from log_conf.logger import logger 

#here shall be functions to build an inventory, iterate through all regions and list the instances. 
#to save api-calls, a file is created the first time a request is made
#TODO: cleanup all inventory files after program is done

def get_instances() -> InstanceContainer:
    try:
        cache_file = "exoscan/lib/controls/compute/instances/instance.inventory.json"
        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                json_data = json.load(f)
        else: 
            logger.info("Creating Inventory of instances...")
            auth = authenticate()
            all_instances = []
            regions = return_regions()
        
            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/instance", auth=auth).json()
                all_instances.extend(response.get("instances", []))
            
            json_data = {"instances": all_instances}

            with open(cache_file, "w") as f:
                json.dump(json_data, f, indent=2)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

    # ✅ Let Pydantic do the parsing
    return InstanceContainer.parse_obj(json_data)


