import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import Instance, InstanceContainer
from provider.return_regions import return_regions
from log_conf.logger import logger 

#here shall be functions to build an inventory, iterate through all regions and list the instances. 
#to save api-calls, a file is created the first time a request is made
#TODO: cleanup all inventory files after program is done

CACHE_FILE = "exoscan/lib/controls/compute/instances/instance.inventory.json"

def get_instances(
        instance_id: str = None
) -> InstanceContainer | Instance:
    try: 
        if instance_id: #if function is called with specific ID (recursively or otherwise)
            if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as f:
                    json_data = json.load(f)

                for instance in json_data.get("instances", []): #if instance is already in cache, return it (if only one instance is needed by an control)
                    if instance.get("id") == instance_id:
                        return Instance.model_validate(instance)
                
            else: #else not required, keeping it for readability 
                regions = return_regions()
                auth = authenticate()
                detail_response = None
                for region in regions:
                    detail_url = f"https://api-{region}.exoscale.com/v2/instance/{instance_id}"
                    detail_response = requests.get(detail_url, auth=auth)
                    if detail_response:
                        instance_data = detail_response.json()
                        instance_data["region"] = region
                        return Instance.model_validate(instance_data) #return details of instance if not yet in cache
                raise Exception(f"Instance ID {instance_id} not found.")

        #if not called with specific instance        
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                json_data = json.load(f)
        else: 
            logger.info("Creating Inventory of instances...")
            regions = return_regions()
            auth = authenticate()

            all_instances = []
            
            #get list of all instances, extract ID and get details based on this reference
            for region in regions: 
                response = requests.get(f"https://api-{region}.exoscale.com/v2/instance", auth=auth).json()
                if response: #maybe no instances in region
                    for instance in response.get("instances", []):
                        instance["region"] = region
                        all_instances.append(instance)
            json_data = {"instances": all_instances}
            container = InstanceContainer.model_validate({"instances": all_instances})

            #write to cache file
            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)
            return container
        return InstanceContainer.model_validate(json_data)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

    


