import argparse

def parse():
    allowed_categories = ["cdn", "compute", "dbaas", "dns", "iam", "organization", "sks", "storage"]

    parser = argparse.ArgumentParser(description= "To use this exoscale scanning tool, provide an API-Key in provider/credentials.txt. Default behaviour is scanning of all resources.")
    parser.add_argument("-v", "--Verbose", action="store_true" , help="Set logging level in stdout to INFO")
    parser.add_argument("-l", "--ListAssets", action="store_true", help="Lists all assets found in the provided account and saves them to a file.")
    parser.add_argument("-c","--OnlyCategory",metavar="category",choices=allowed_categories, help=f"Only scan category: {", ".join(allowed_categories)}"
    )

    parser.parse_args()
    args = parser.parse_args()

    return args