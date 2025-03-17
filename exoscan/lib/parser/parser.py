import argparse

def parse():
    parser = argparse.ArgumentParser(description= "To use this exoscale scanning tool, provide an API-Key in provider/credentials.txt")
    parser.add_argument("-v", "--Verbose", action="store_true" , help="Set logging level in stdout to INFO")
    parser.add_argument("-l", "--ListAssets", action="store_true", help="Lists all assets found in the provided account and saves them to a file.")
    parser.parse_args()

    args = parser.parse_args()
    print(args)
    return args