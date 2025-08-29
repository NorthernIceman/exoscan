import argparse

def parse():

    parser = argparse.ArgumentParser(description= "To use this exoscale scanning tool, provide an API-Key in provider/credentials.txt. Default behaviour is scanning of all resources.")
    parser.add_argument("-v", "--Verbose", action="store_true" , help="Set logging level in stdout to INFO")
 
    parser.parse_args()
    args = parser.parse_args()

    return args