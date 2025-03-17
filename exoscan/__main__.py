#!/usr/bin/env python3
from provider.exoscale_provider import authenticate
from log_conf.logger import logger, set_logging_config
from exoscan.lib.banner import print_banner
from exoscan.lib.parser import parser
import requests, sys

def exoscan():
    #do not produce list of assets in standard-function
    list_assets = 0

    #print banner and parsing instructions
    print_banner()
    args = parser.parse()

    #set logging level
    set_logging_config(args.Verbose)

    #verify if API-Access is successful 
    logger.info("Trying to log into exoscale with provided credentials...")
    auth = authenticate() #retreive auth header for response
    response = requests.get("https://api-ch-gva-2.exoscale.com/v2/", auth=auth)
    if response.status_code == 204:
        logger.info("Authentication successful.")
    else:
        logger.error("Authentication not successful. Aborting...")
        sys.exit()

    #start checks

    
    #ToDo: 
    # take compliance file ? 
    # execute checks

if __name__ == "__main__":
    exoscan()