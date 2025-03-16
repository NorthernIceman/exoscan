#!/usr/bin/env python3
from provider.exoscale_provider import authenticate
from log_conf.logger import logger, set_logging_config
import requests

def exoscan():
    set_logging_config()
    logger.info("Trying to log into exoscale with provided credentials...")
    auth = authenticate()
    response = requests.get("https://api-ch-gva-2.exoscale.com/v2/ssh-key", auth=auth)
    print(response.json())
      
    #ToDo: 
    # Take creds, 
    # Use api: https://github.com/exoscale/python-exoscale/actions
    #create read only account, 
    # take compliance file 
    # execute checks

if __name__ == "__main__":
    exoscan()