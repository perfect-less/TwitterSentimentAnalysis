import sys

import twint


def CreateConfig():
    config = twint.Config()
    config.Search = "AbrahamAccords"
    config.Lang = "en"
    config.Limit = 10
    config.Store_json = True
    config.Output = "custom_out.json"

    return config

def main ():
    conf = CreateConfig()
    twint.run.Search(conf)


if __name__ == "__main__":
    sys.exit(main())