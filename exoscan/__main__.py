#!/usr/bin/env python3
from provider.exoscale_provider import authenticate
from log_conf.logger import logger, set_logging_config
from exoscan.lib.banner import print_banner
from exoscan.lib.parser import parser
from exoscan.lib.controls.controls_loader import fetch_controls
from exoscan.lib.controls.execute_controls import execute_controls
import requests, sys

def exoscan():
    #do not produce list of assets in standard-function
    #list_assets = 0

    #print banner and parsing instructions
    print_banner()

    args = parser.parse()
    #set logging level
    set_logging_config(args.Verbose)

    auth = authenticate() #retreive auth header for response

    controls_to_execute = fetch_controls()
    execute_controls(controls_to_execute)

    #ToDo: 
    # execute checks

if __name__ == "__main__":
    exoscan()