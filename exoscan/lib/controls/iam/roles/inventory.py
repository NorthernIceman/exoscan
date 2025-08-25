import requests, os, json, sys
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import IAMRole, IAMRoleContainer
from log_conf.logger import logger 

CACHE_FILE = "exoscan/lib/controls/iam/roles/roles.inventory.json"

def get_roles(
        role_id: str = None
) -> IAMRoleContainer | IAMRole:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("IAM Role cache not found. Creating full inventory...")
            auth = authenticate()

            all_roles = []

            response = requests.get(f"https://api-ch-dk-2.exoscale.com/v2/iam-role", auth=auth)
            if response.status_code == 200:
                for role in response.json().get("iam-roles", []):
                    details_response  = requests.get(f"https://api-ch-dk-2.exoscale.com/v2/iam-role/{role["id"]}", auth=auth)
                    if details_response.status_code == 200:
                        all_roles.append(details_response.json())
                            
            container = IAMRoleContainer.model_validate({"iam-roles": all_roles})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Load from cache now (it exists for sure)
        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if role_id:
            for role in json_data.get("iam-roles", []):
                if role.get("id") == role_id:
                    return IAMRole.model_validate(role)

            raise Exception(f"Role ID '{role_id}' not found in cached inventory.")

        return IAMRoleContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
