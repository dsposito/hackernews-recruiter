from BeautifulSoup import BeautifulSoup
from pprint import PrettyPrinter
import requests

def getNormalizedMetas():
    return {
        "email": [],
        "github": [],
        "languages": [],
        "linkedin": [],
        "location": [],
        "relocate": ["relocation", "willing to relocate"],
        "remote": [],
        "resume": ["resume/cv", "r&#233;sum&#233;", "resume&#x2f;cv", "r&#233;sum&#233;&#x2f;cv"],
        "site": ["blog", "portfolio", "website"],
        "stackoverflow": [],
        "technologies": ["frameworks", "tech", "tools"]
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


pp = PrettyPrinter(depth=6)

url = 'https://news.ycombinator.com/item?id=12016570'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html)
table = soup.find('table', attrs={'class': 'comment-tree'})

candidates = []
for row in table.findAll('table'):
    candidate = {}

    # @TODO Grab location from initial span
    for line in row.findAll('p'):
        meta = line.text.split(':')
        if (len(meta) == 1):
            continue

        name = meta[0].strip().lower().encode("ascii", "xmlcharrefreplace")

        if isSupportedMeta(name):
            name = getNormalizedMeta(name)
            value = meta[1].strip().encode("ascii", "xmlcharrefreplace")

            candidate[name] = value

    # Add candidate to list of candidates if it contains at least 2 supported metas.
    if (len(candidate) > 1):
        candidates.append(candidate)

        pp.pprint(candidate)
        print "\n"


    #pp.pprint(candidates)

    # comment = row.find('span', attrs={'class': 'comment'})
    # print row.prettify()
