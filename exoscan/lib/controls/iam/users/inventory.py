import requests, os, json, sys, tempfile
from provider.exoscale_provider import authenticate
from exoscan.lib.controls.models import IAMUser, IAMUserContainer
from log_conf.logger import logger 

_temp_cache = tempfile.NamedTemporaryFile(
    prefix="iam_users_inventory_", suffix=".json", delete=False
)
CACHE_FILE = _temp_cache.name

def get_users(
        user_id: str = None
) -> IAMUserContainer | IAMUser:
    try:
        if not os.path.exists(CACHE_FILE):
            logger.info("IAM Users cache not found. Creating full inventory...")
            auth = authenticate()

            all_users = []

            response = requests.get(f"https://api-ch-dk-2.exoscale.com/v2/user", auth=auth)
            if response.status_code == 200:
                all_users.extend(response.json().get("users", []))
                            
            container = IAMUserContainer.model_validate({"users": all_users})

            with open(CACHE_FILE, "w") as f:
                json.dump(container.model_dump(mode="json", by_alias=True), f, indent=2)

        # Load from cache now (it exists for sure)
        with open(CACHE_FILE, "r") as f:
            json_data = json.load(f)

        if user_id:
            for user in json_data.get("users", []):
                if user.get("id") == user_id:
                    return IAMUser.model_validate(user)

            raise Exception(f"User ID '{user_id}' not found in cached inventory.")

        return IAMUserContainer.model_validate(json_data)

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
