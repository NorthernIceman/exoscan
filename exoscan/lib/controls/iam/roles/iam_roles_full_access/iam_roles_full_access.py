import sys
from exoscan.lib.controls.iam.roles.inventory import get_roles
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: iam_roles_full_access")
    try: 
        all_roles = get_roles()
        if not all_roles.roles: 
            logger.info("No roles found. Skipping Control iam_roles_full_access...")
            return

        findings = []
        found_roles = []

        for role in all_roles.roles:
            if role.policy.default_service_strategy == "allow":
                services = role.policy.services or {}
                # If no services, it's full access
                if not services:
                    found_roles.append(role.name)
                    continue
                # assume all policies allow action; if all services have type "allow" and all rules have action "allow"
                all_allow = True
                for service_obj in services.values():
                    if service_obj.access_type != "allow":
                        all_allow = False
                        break
                    if service_obj.rules:
                        for rule in service_obj.rules:
                            if rule.action != "allow":
                                all_allow = False
                                break
                    if not all_allow:
                        break
                if all_allow:
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