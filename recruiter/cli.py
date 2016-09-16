import json

from argparse import ArgumentParser
from candidate import Candidate
from datetime import datetime
from parser.google import Google as GoogleParser
from parser.hackernews import Hackernews as HackernewsParser
from scraper import Scraper


class CLI(object):
    @classmethod
    def main(cls):
        parser = ArgumentParser(description='Scrapes "Who Wants to be Hired?" HN Posts.')
        parser.add_argument("-s", "--source", help="The source url to scrape.")
        parser.add_argument("-t", "--technologies", nargs="*", help="The technology(ies) to filter on.")
        parser.add_argument("-l", "--location", nargs="*", help="The location(s) to filter on.")
        parser.add_argument("-rel", "--relocate", action='store_true', help="Applies a filter of 'willing to relocate' = Yes.")
        parser.add_argument("-rem", "--remote", action='store_true', help="Applies a filter of 'willing to work remotely' = Yes.")
        args = parser.parse_args()

        filters = {}
        if args.technologies is not None:
            filters[Candidate.META_TECHNOLOGIES] = args.technologies
        if args.location is not None:
            filters[Candidate.META_LOCATION] = args.location
        if args.relocate:
            filters[Candidate.META_RELOCATE] = "Yes"
        if args.remote:
            filters[Candidate.META_REMOTE] = "Yes"

        url = args.source
        url = cls.getDefaultSourceUrl() if url is None else url

        print "\nParsing Source: " + url

        html = Scraper(url).get()
        data = HackernewsParser(html, filters)
        title = data.getTitle()
        candidates = data.getCandidates()

        print "\n" + json.dumps(candidates, indent=4, sort_keys=True)
        print "\nParsed Source: " + title
        print "\nTotal Matches Found: " + str(len(candidates))

    @staticmethod
    def getDefaultSourceUrl():
        month = datetime.now().strftime("%B %Y")
        url = "https://www.google.com/search" \
            + "?as_qdr=all&complete=0" \
            + "&q=hackernews%20who%20wants%20to%20be%20hired%20" + month

        html = Scraper(url).get()

        return GoogleParser(html).getFirstResultUrl()


if __name__ == '__main__':
    CLI.main()
