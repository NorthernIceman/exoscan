import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import SecurityGroup, SecurityGroupContainer
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="security_groups_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

def get_security_groups(
        security_group_id: str = None
) -> SecurityGroupContainer | SecurityGroup:

    try: 
        if not os.path.exists(CACHE_FILE) or os.path.getsize(CACHE_FILE) == 0:
            logger.info("Creating Inventory of Security-Groups...")
            auth = authenticate()

            # with security-groups, region does not matter
            response = requests.get(f"https://api-ch-gva-2.exoscale.com/v2/security-group", auth=auth)
            if response.status_code == 200:
                json_data = response.json()

            sg_container = SecurityGroupContainer.model_validate(json_data)
            with open(CACHE_FILE, "w") as f:
                json.dump(sg_container.model_dump(mode="json", by_alias=True), f, indent=2)

        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if security_group_id:
            for sg in json_data.get("security-groups", []):
                if sg.get("id") == security_group_id:
                    return SecurityGroup.model_validate(sg)
            raise Exception(
                f"Private Network ID '{security_group_id}' not found in cached inventory."
            )
        
        return SecurityGroupContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)