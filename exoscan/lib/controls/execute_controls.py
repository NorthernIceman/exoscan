import importlib
from log_conf.logger import logger
from pathlib import Path

def execute_controls(controls_modules_path):
    logger.info("Executing controls...")
    findings = []
    try: 
        for module in controls_modules_path:
            control = importlib.import_module(f"{module}")

            parts = module.split(".")

            *base_path, filename = parts

            metadata_path = Path("/".join(base_path)) / f"{filename}.metadata.json"
            control_findings = control.execute_logic(metadata_path)
            if control_findings:
                findings.extend(control_findings)
        return findings
    except Exception as error: 
        logger.error(
            f"{error.__class__.__name__}[{error.__traceback__.tb_lineno}] -- {error}"
        )
