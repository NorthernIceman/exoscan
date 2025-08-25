import sys
from exoscan.lib.controls.iam.roles.inventory import get_roles
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: iam_roles_iam_full_access")
    try: 
        all_roles = get_roles()
        if not all_roles.roles: 
            logger.info("No roles found. Skipping Control iam_roles_iam_full_access...")
            return

        findings = []
        found_roles = []

        for role in all_roles.roles:
            iam_service = role.policy.services.get("iam") if role.policy.services else None
            # If default strategy is allow and no IAM service, or IAM service exists and has no rules
            if (role.policy.default_service_strategy == "allow" and not iam_service) or (iam_service and not iam_service.rules):
                found_roles.append(role.name)

        if found_roles:
                roles_str = "\n - ".join(found_roles)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Roles: \n - {str(roles_str)}"
                ))
        return findings

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return