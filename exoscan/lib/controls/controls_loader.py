
from exoscan.lib.controls.utils import import_all_controls
from log_conf.logger import logger

#tasks function in utils to get it all directories with controls in them, then parses them to modules and passes them to main()
def fetch_controls() -> set: 
    try:
        logger.info("Fetching controls...")
        controls_modules_path = []
        controls = import_all_controls()

        for control in controls: 
            controls_modules_path.append('.'.join((f"{control[1]}\\{control[0]}").split("\\")[-7:]))

        return controls_modules_path
    except Exception as error:
        logger.error(
            f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}"
        )
        return controls_modules_path