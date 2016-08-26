import argparse
from BeautifulSoup import BeautifulSoup
import datetime
from HTMLParser import HTMLParser
import json
import requests

META_EMAIL = "email"
META_GITHUB = "github"
META_LANGUAGES = "languages"
META_LINKEDIN = "linkedin"
META_LOCATION = "location"
META_RELOCATE = "relocate"
META_REMOTE = "remote"
META_RESUME = "resume"
META_SITE = "site"
META_STACKOVERFLOW = "stackoverflow"
META_TECHNOLOGIES = "technologies"


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


def getMetaFromString(string):
    if string is None:
        return False

    # Remove any HTML tags and rejoin matches as a string.
    meta = "".join(string.findAll(text=True))
    meta = meta.split(": ")

    if (len(meta) == 1):
        return False

    # Normalize the string (including converting any UTF8 characters to html entities).
    name = meta[0].strip().lower().encode("ascii", "xmlcharrefreplace")

    if not isSupportedMeta(name):
        return False

    name = getNormalizedMeta(name)
    value = HTMLParser().unescape(meta[1].strip())

    return {
        "name": name,
        "value": getNormalizedMetaValue(name, value)
    }


def getNormalizedMetas():
    return {
        META_EMAIL: [],
        META_GITHUB: [],
        META_LANGUAGES: [],
        META_LINKEDIN: [],
        META_LOCATION: [],
        META_RELOCATE: [
            "relocation",
            "willing to relocate"
        ],
        META_REMOTE: [],
        META_RESUME: [
            "resume/cv",
            "r&#233;sum&#233;",
            "resume&#x2f;cv",
            "r&#233;sum&#233;&#x2f;cv"
        ],
        META_SITE: [
            "blog",
            "portfolio",
            "website"
        ],
        META_STACKOVERFLOW: [],
        META_TECHNOLOGIES: [
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


def getNormalizedMetaValue(meta, value):
    if meta in [META_RELOCATE, META_REMOTE]:
        if "Yes" in value: return "Yes"
        if "No" in value or "Nope" in value: return "No"

    return value


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

    # Grab span tag for Location meta.
    location = getMetaFromString(row.find("span", attrs={"class": "c00"}))
    if location:
        candidate[location["name"]] = location["value"]

    # Grab p tags for remaining metas.
    for line in row.findAll("p"):
        meta = getMetaFromString(line)
        if (meta):
            candidate[meta["name"]] = meta["value"]

    # Add candidate to list of candidates if it contains at least 2 supported metas.
    if (len(candidate) > 1):
        candidates.append(candidate)

print "\nTotal Matches Found: " + str(len(candidates))
print "\n" + json.dumps(candidates, indent=4, sort_keys=True)
