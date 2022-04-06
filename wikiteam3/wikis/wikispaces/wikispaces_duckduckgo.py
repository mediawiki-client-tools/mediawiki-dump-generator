#!/usr/bin/env python3

# Copyright (C) 2018 WikiTeam developers
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import random
import re
import sys
import time
from urllib.parse import unquote

import requests
from dump_generator.user_agent import UserAgent


def main():
    requests.Session().headers = {"User-Agent": str(UserAgent())}

    words = []
    with open("words.txt") as words_file:
        words = words_file.read().strip().splitlines()
    random.shuffle(words)
    print("Loaded %d words from file" % (len(words)))
    # words = words + ['%d' % (i) for i in range(1900, 1980, 10)]
    wikis = []
    with open("wikispaces-duckduckgo.txt") as wikispaces_duckduckgo_file:
        wikis = wikispaces_duckduckgo_file.read().strip().splitlines()
        wikis.sort()
    print("Loaded %d wikis from file" % (len(wikis)))

    for i in range(1, 100):
        random.shuffle(words)
        for word in words:
            print("Word", word)
            word_ = re.sub(" ", "+", word)
            url = ""
            r = random.randint(0, 10)
            if r == 0:
                url = "https://duckduckgo.com/html/?q=%s%%20site:wikispaces.com" % (
                    word_
                )
            elif r == 1:
                url = "https://duckduckgo.com/html/?q=%s%%20wikispaces.com" % (word_)
            elif r == 2:
                url = "https://duckduckgo.com/html/?q={}%20{}%20wikispaces.com".format(
                    word_,
                    random.randint(100, 3000),
                )
            elif r == 3:
                url = "https://duckduckgo.com/html/?q={}%20{}%20wikispaces.com".format(
                    random.randint(100, 3000),
                    word_,
                )
            else:
                url = "https://duckduckgo.com/html/?q={}%20{}%20wikispaces.com".format(
                    word_,
                    random.randint(100, 3000),
                )
            print("URL search", url)
            try:
                html = requests.Session().get(url).read().decode("utf-8")
            except Exception:
                print("Search error")
                sys.exit()
            html = unquote(html)
            match = re.findall(r"://([^/]+?\.wikispaces\.com)", html)
            for wiki in match:
                wiki = "https://" + wiki
                if wiki not in wikis:
                    wikis.append(wiki)
                    wikis.sort()
                    print(wiki)
            with open("wikispaces-duckduckgo.txt", "w") as wikispaces_duckduckgo_file:
                wikis2 = []
                for wiki in wikis:
                    wiki = re.sub(r"https://www\.", "https://", wiki)
                    if wiki not in wikis2:
                        wikis2.append(wiki)
                wikis = wikis2
                wikis.sort()
                wikispaces_duckduckgo_file.write("\n".join(wikis))
            print("%d wikis found" % (len(wikis)))
            sleep = random.randint(5, 20)
            print("Sleeping %d seconds" % (sleep))
            time.sleep(sleep)


if __name__ == "__main__":
    main()