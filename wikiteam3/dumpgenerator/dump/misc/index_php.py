import os

from wikiteam3.dumpgenerator.cli import Delay
from wikiteam3.dumpgenerator.config import Config
from wikiteam3.utils import removeIP


def saveIndexPHP(config: Config = None, session=None):
    """Save index.php as .html, to preserve license details available at the botom of the page"""

    if os.path.exists(f"{config.path}/index.html"):
        print("index.html exists, do not overwrite")
    else:
        print("Downloading index.php (Main Page) as index.html")
        r = session.post(url=config.index, params=None, timeout=10)
        raw = str(r.text)
        Delay(config=config, session=session)
        raw = removeIP(raw=raw)
        with open(f"{config.path}/index.html", "w", encoding="utf-8") as outfile:
            outfile.write(raw)
