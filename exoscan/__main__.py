#!/usr/bin/env python3
from provider.exoscale_provider import authenticate
from log_conf.logger import logger, set_logging_config
from exoscan.lib.banner import print_banner
from exoscan.lib.parser import parser
from exoscan.lib.controls.controls_loader import fetch_controls
from exoscan.lib.controls.execute_controls import execute_controls

def exoscan():
    #do not produce list of assets in standard-function
    #list_assets = 0

    #print banner and parsing instructions
    print_banner()

    args = parser.parse()
    #set logging level
    set_logging_config(args.Verbose)

    findings = []
    controls_to_execute = fetch_controls()
    results = execute_controls(controls_to_execute)
    if results: findings.extend(results)

    for finding in findings:
        finding.print_finding()

    #TODO: cleanup all inventory files after program is done

if __name__ == "__main__":
    exoscan()