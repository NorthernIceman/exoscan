import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import Instance, InstanceContainer, InstanceType, InstanceTypeContainer, Template, TemplateContainer
from provider.return_regions import return_regions
from log_conf.logger import logger 

#here shall be functions to build an inventory, iterate through all regions and list the instances. 
#to save api-calls, a file is created the first time a request is made
#TODO: cleanup all inventory files after program is done

CACHE_FILE = "exoscan/lib/controls/compute/instances/instance.inventory.json"
CACHE_FILE_TYPE = "exoscan/lib/controls/compute/instances/instance_type.inventory.json"
CACHE_FILE_TEMPLATE = "exoscan/lib/controls/compute/instances/templates.inventory.json"

def get_instances(
        instance_id: str = None
) -> InstanceContainer | Instance:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("Instance cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_instances = []

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/instance", auth=auth)
                if response.status_code == 200:
                    for instance in response.json().get("instances", []):
                        instance["region"] = region
                        all_instances.append(instance)

            container = InstanceContainer.model_validate({"instances": all_instances})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Load from cache now (it exists for sure)
        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if instance_id:
            for instance in json_data.get("instances", []):
                if instance.get("id") == instance_id:
                    return Instance.model_validate(instance)

            raise Exception(f"Instance ID '{instance_id}' not found in cached inventory.")

        return InstanceContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)

def get_instance_types(
        instance_type: str = None
) -> InstanceTypeContainer | InstanceType:   
    try:
        # Always check for cache; if not exists, build full inventory
        if not os.path.exists(CACHE_FILE_TYPE):
            logger.info("Instance type cache not found. Creating full inventory...")
            regions = return_regions()
            auth = authenticate()

            all_instance_types = []
            seen_ids = set()

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/instance-type", auth=auth)
                if response.status_code == 200:
                    for inst_type in response.json().get("instance-types", []):
                        inst_id = inst_type.get("id")
                        if inst_id and inst_id not in seen_ids:
                            inst_type["region"] = region
                            all_instance_types.append(inst_type)
                            seen_ids.add(inst_id)

            container = InstanceTypeContainer.model_validate({"instance-types": all_instance_types})

            with open(CACHE_FILE_TYPE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Cache file exists now — load it
        with open(CACHE_FILE_TYPE, "r") as f:
            json_data = json.load(f)

        if instance_type:
            for inst_type in json_data.get("instance-types", []):
                if inst_type.get("id") == instance_type:
                    return InstanceType.model_validate(inst_type)
            raise Exception(f"Instance Type '{instance_type}' not found in cached inventory.")

        return InstanceTypeContainer.model_validate(json_data)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)


def get_instance_templates(
    template_id: str = None
) -> TemplateContainer | Template:
    try:
        if not os.path.exists(CACHE_FILE_TEMPLATE):
            logger.info("Instance template cache not found. Creating full inventory...")
            auth = authenticate()

            all_templates = []


            response = requests.get(f"https://api-ch-gva-2.exoscale.com/v2/template", auth=auth)
            if response.status_code == 200:
                for template in response.json().get("templates", []):
                    all_templates.append(template)

            container = TemplateContainer.model_validate({"templates": all_templates})

            with open(CACHE_FILE_TEMPLATE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)


        with open(CACHE_FILE_TEMPLATE, "r") as f:
            json_data = json.load(f)


        if template_id:
            for template in json_data.get("instance-templates", []):
                if template.get("id") == template_id:
                    return Template.model_validate(template)

            return False


        return TemplateContainer.model_validate(json_data)
    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
