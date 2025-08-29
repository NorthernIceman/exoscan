#!/usr/bin/env python3
from provider.exoscale_provider import authenticate
from log_conf.logger import logger, set_logging_config
from exoscan.lib.banner import print_banner
from parser import parser
from exoscan.lib.controls.controls_loader import fetch_controls
from exoscan.lib.controls.execute_controls import execute_controls

def exoscan():

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

if __name__ == "__main__":
    exoscan()