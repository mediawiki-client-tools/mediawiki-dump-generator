import re
import requests
import sys

from .delay import delay
from .domain import Domain
from .exceptions import PageMissingError
from .log_error import logerror
from .page_titles import readTitles
from .page_xml import getXMLPage
from .util import cleanXML
from .xml_header import getXMLHeader
from .xml_revisions import getXMLRevisions
from .xml_truncate import truncateXMLDump


def generateXMLDump(config: dict, titles: str, start: str = ""):
    """Generates a XML dump for a list of titles or from revision IDs"""
    # TODO: titles is now unused.

    header, config = getXMLHeader(config)
    footer = "</mediawiki>\n"  # new line at the end
    xmlfilename = "%s-%s-%s.xml" % (
        Domain(config).to_prefix(),
        config["date"],
        config["current-only"] and "current-only" or "history",
    )
    xmlfile = ""
    lock = True

    if config["revisions"]:
        if start != "":
            print("WARNING: will try to start the download from title: %s" % start)
            xmlfile = open(
                "%s/%s" % (config["path"], xmlfilename), "a", encoding="utf-8"
            )
        else:
            print("")
            print("Retrieving the XML for every page from the beginning")
            xmlfile = open("%s/%s" % (config["path"], xmlfilename), "wb")
            xmlfile.write(header)
        try:
            r_timestamp = "<timestamp>([^<]+)</timestamp>"
            for xml in getXMLRevisions(config, start=start):
                numrevs = len(re.findall(r_timestamp, xml))
                # Due to how generators work, it's expected this may be less
                # TODO: get the page title and reuse the usual format "X title, y edits"
                print("        %d more revisions exported" % numrevs)
                xml = cleanXML(xml=xml)
                xmlfile.write(str(xml))
        except AttributeError as e:
            print(e)
            print("This API library version is not working")
            sys.exit()
    else:
        if start not in {"", "start"}:
            print("")
            print('Retrieving the XML for every page from "%s"' % (start))
            print(
                "Removing the last chunk of past XML dump: it is probably incomplete."
            )
            truncateXMLDump("%s/%s" % (config["path"], xmlfilename))
        else:
            print("")
            print("Retrieving the XML for every page from the beginning")
            # requested complete xml dump
            lock = False
            xmlfile = open(
                "%s/%s" % (config["path"], xmlfilename), "w", encoding="utf-8"
            )
            xmlfile.write(header)
            xmlfile.close()

        xmlfile = open("%s/%s" % (config["path"], xmlfilename), "a", encoding="utf-8")
        count = 1
        for title in readTitles(config, start):
            if not title:
                continue
            if title == start:  # start downloading from start, included
                lock = False
            if lock:
                continue
            delay(config)
            if count % 10 == 0:
                print("")
                print("->  Downloaded %d pages" % (count))
            try:
                for xml in getXMLPage(config=config, title=title, verbose=True):
                    xml = cleanXML(xml=xml)
                    xmlfile.write(str(xml))
            except PageMissingError:
                logerror(
                    config,
                    text=u'The page "%s" was missing in the wiki (probably deleted)'
                    % title,
                )
            # here, XML is a correct <page> </page> chunk or
            # an empty string due to a deleted page (logged in errors log) or
            # an empty string due to an error while retrieving the page from server
            # (logged in errors log)
            count += 1

    xmlfile.write(footer)
    xmlfile.close()
    print("XML dump saved at...", xmlfilename)
