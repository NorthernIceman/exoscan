import requests, os, json, sys
from provider.exoscale_provider import authenticate, return_regions
from exoscan.lib.controls.models import Template, TemplateContainer
from log_conf.logger import logger 

CACHE_FILE_TEMPLATE = "exoscan/lib/controls/compute/templates/templates.inventory.json"

def get_instance_templates(
    template_id: str = None
) -> TemplateContainer | Template:
    try:
        if not os.path.exists(CACHE_FILE_TEMPLATE):
            logger.info("Instance template cache not found. Creating full inventory...")
            auth = authenticate()
            regions = return_regions()
            all_templates = []
            seen_ids = set()

            for region in regions:
                response = requests.get(f"https://api-{region}.exoscale.com/v2/template", auth=auth)
                if response.status_code == 200:
                    for template in response.json().get("templates", []):
                        temp_id = template.get("id")
                        if temp_id and temp_id not in seen_ids:
                            all_templates.append(template)
                            seen_ids.add(temp_id)

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
