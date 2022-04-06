import json
import sys


def load_config(config: dict, config_filename: str) -> dict:
    """Load config file"""

    try:
        with open(
            "{}/{}".format(config["path"], config_filename), encoding="utf-8"
        ) as infile:
            config = json.load(infile)
    except Exception:
        print("There is no config file. we can't resume. Start a new dump.")
        sys.exit()

    return config


def save_config(config: dict, config_filename: str):
    """Save config file"""

    with open(
        "{}/{}".format(config["path"], config_filename), "w", encoding="utf-8"
    ) as outfile:
        json.dump(config, outfile)