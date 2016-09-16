# hackernews-recruiter
This CLI tool scrapes "Who Wants to be Hired?" Hacker News posts to make it easier to find developers that are looking for new opportunities. Candidates can be filtered by tech skills and geographic location.

## Installation

This project is intended to be used with Python 2.7.*; it has not been tested with Python 3.

Run the following command to install the project's dependencies:

	$ pip install -r requirements.txt


## Usage

Use the `-s` or `--source` param to specify a Hacker News thread URL to parse.
If none is provided, the current month's Hacker News post will be parsed.

	$ ./recruit --source https://news.ycombinator.com/item?id=10152811

**Example Output**
```
Parsing Source: https://news.ycombinator.com/item?id=10152811

[
    {
        "email": "angieyeh24@gmail.com",
        "location": "Los Angeles, CA",
        "relocate": "Yes",
        "remote": "No",
        "resume": "https://docs.google.com/document/d/1Rlb3-gbr3nhfBAaxyJOwRlEC...",
        "technologies": "Javascript, Node, React, Angular, MySQL, MongoDB, HTML/CSS, Mocha/Tape for testing"
    },
    {
        "email": "nikitaame@gmail.com",
        "location": "Los Angeles, CA",
        "relocate": "Yes",
        "remote": "No",
        "resume": "Upon Request",
        "technologies": "iOS(Swift & Objective C), Android(Java), Web (HTML, CSS, Javascript, C, C++, SQL, OpenCV"
    },
    {
        "email": "philt300 at yahoo",
        "location": "Greater Los Angeles Area, CA",
        "relocate": "Yes",
        "remote": "Yes",
        "resume": "https://www.linkedin.com/in/theoapps",
        "technologies": "Swift, Objective-C, iOS, Java, J2EE, Android, Javascript, C++, Git"
    },
    ...
]

Parsed Source: Ask HN: Who wants to be hired? (July 2016)

Total Matches Found: 130
```


Results can be filtered on various candidate meta data. For example, to filter results to candidates with "PHP" skills in the "Technologies" meta key:

	$ ./recruit --technologies "PHP"


One or more values may be provided for each meta filter. The following will return all candidates with "PHP" OR "Python" skills in the "Technologies" meta key:

	$ ./recruit --technologies "PHP" "Python"


The following will return all candidates with "Los Angeles" in the "Location" meta key OR candidates that are willing to relocate (Relocate=Yes):

	$ ./recruit --location "Los Angeles" --relocate


Run the following command to see all possible parameters for `scraper.py`:

	$ ./recruit --help
