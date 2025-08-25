import sys
from exoscan.lib.controls.iam.users.inventory import get_users
from exoscan.lib.controls.models import Finding
from log_conf.logger import logger

def execute_logic(metadata_path):
    logger.info("Executing Control: iam_users_mfa_enabled")
    try: 
        all_users = get_users()
        if not all_users.users: 
            logger.info("No users found. Skipping Control iam_users_mfa_enabled...")
            return

        findings = []
        found_users = []

        for user in all_users.users:
            if user.two_factor_authentication != True:
                 found_users.append(user.id)
        if found_users:
                users_str = "\n - ".join(found_users)
                findings.append(Finding.from_metadata(
                    metadata_file= metadata_path,
                    resource_description=f"Users: \n - {str(users_str)}"
                ))
        return findings

    except Exception as error:
        logger.error(f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}")
        sys.exit(1)
    return