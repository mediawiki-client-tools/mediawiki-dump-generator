import json

import requests

from wikiteam3.dumpgenerator.test.test_config import get_config
from wikiteam3.dumpgenerator.config import Config

from typing import cast

from .site_info import saveSiteInfo


def test_mediawiki_version_match():
    config: Config = cast(Config, get_config("1.45.1"))
    if config:
        sess = requests.Session()
        saveSiteInfo(config, sess)
        with open(f"{config.path}/siteinfo.json") as f:
            siteInfoJson = json.load(f)
        assert siteInfoJson["query"]["general"]["generator"] == "MediaWiki 1.45.1"
