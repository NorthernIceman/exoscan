import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import SecurityGroup, SecurityGroupContainer
from log_conf.logger import logger 

#TODO: cleanup all inventory files after program is done

CACHE_FILE = "exoscan/lib/controls/compute/security_groups/security_groups.inventory.json"

def get_security_groups(
        security_group_id: str = None
) -> SecurityGroupContainer | SecurityGroup:

    try: 

        if os.path.exists(CACHE_FILE):
                with open(CACHE_FILE, "r") as f:
                    json_data = json.load(f)
        else:
            logger.info("Creating Inventory of Security-Groups...")
            auth = authenticate()

            # with security-groups, region does not matter
            json_data = requests.get(f"https://api-ch-gva-2.exoscale.com/v2/security-group", auth=auth).json()
            with open(CACHE_FILE, "w") as f:
                json.dump(json_data, f, indent=2)

        sg_container = SecurityGroupContainer.model_validate(json_data)

        if security_group_id:
            for sg in sg_container.security_groups:
                if sg.id == security_group_id:
                    return sg
        else: 
            return sg_container

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)



