import argparse
from BeautifulSoup import BeautifulSoup
import datetime
from HTMLParser import HTMLParser
import json
import requests


def getDefaultSourceUrl():
    month = datetime.datetime.now().strftime("%B")
    url = "https://www.google.com/search" \
        + "?as_qdr=all&complete=0" \
        + "&q=hackernews%20who%20wants%20to%20be%20hired%20" + month

    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html)
    results = soup.find("div", attrs={"id": "search"})
    result = results.find("cite")

    return result.text


def getNormalizedMetas():
    return {
        "email": [],
        "github": [],
        "languages": [],
        "linkedin": [],
        "location": [],
        "relocate": [
            "relocation",
            "willing to relocate"
        ],
        "remote": [],
        "resume": [
            "resume/cv",
            "r&#233;sum&#233;",
            "resume&#x2f;cv",
            "r&#233;sum&#233;&#x2f;cv"
        ],
        "site": [
            "blog",
            "portfolio",
            "website"
        ],
        "stackoverflow": [],
        "technologies": [
            "frameworks",
            "tech",
            "tools"
        ]
    }


def getNormalizedMeta(meta):
    for name, aliases in getNormalizedMetas().iteritems():
        if meta == name or meta in aliases:
            return name

    return meta


def isSupportedMeta(meta):
    if len(meta) < 4:
        return False

    for name, aliases in getNormalizedMetas().iteritems():
        if meta == name or meta in aliases:
            return True

    return False


# @TODO This will be non-static method on the base Dictionary object
def hasMetaValue(meta, value):
    if len(meta) < 4:
        return False

    for name, aliases in getNormalizedMetas().iteritems():
        if meta == name or meta in aliases:
            return True

    return False


parser = argparse.ArgumentParser(description='Scrapes "Who Wants to be Hired?" HN Posts.')
parser.add_argument("-s", "--source", help="The source url to scrape.")
args = parser.parse_args()

url = args.source
url = getDefaultSourceUrl() if url is None else url

print "\nParsing Source: " + url

response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)
table = soup.find("table", attrs={"class": "comment-tree"})

candidates = []
for row in table.findAll("table"):
    candidate = {}

    # @TODO Grab location from initial span
    for line in row.findAll("p"):
        # Remove any HTML tags and rejoin matches as a string.
        meta = "".join(line.findAll(text=True))
        meta = meta.split(": ")

        if (len(meta) == 1):
            continue

        # Normalize the string (including converting any UTF8 characters to html entities).
        name = meta[0].strip().lower().encode("ascii", "xmlcharrefreplace")

        if isSupportedMeta(name):
            name = getNormalizedMeta(name)
            value = HTMLParser().unescape(meta[1].strip())

            candidate[name] = value

    # Add candidate to list of candidates if it contains at least 2 supported metas.
    if (len(candidate) > 1):
        candidates.append(candidate)

print "\nTotal Matches Found: " + str(len(candidates))
print "\n" + json.dumps(candidates, indent=4, sort_keys=True)
