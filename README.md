# hackernews-recruiter
Scrapes "Who Wants to be Hired?" HN Posts

## Installation

This project is intended to be used with Python 2.7.*; it has not been tested with Python 3.

Run the following command to install the project's dependencies:
	$ pip install -r requirements.txt


## Usage

Use the `-s` or `--source` param to specify a Hacker News thread URL to parse.
If none is provided, the current month's Hacker News post will be parsed.

	$ python scraper.py --source https://news.ycombinator.com/item?id=12016570


Results can be filtered on various candidate meta data. For example, to filter results to candidates with "PHP" skills in the "Technologies" meta key:

	$ python scraper.py --source https://news.ycombinator.com/item?id=12016570 --technologies "PHP"


One or more values may be provided for each meta filter. The following will return all candidates with "PHP" OR "Python" skills in the "Technologies" meta key:

	$ python scraper.py --source https://news.ycombinator.com/item?id=12016570 --technologies "PHP" "Python"


Run the following command to see all possible parameters for `scraper.py`:

	$ python scraper.py --help
