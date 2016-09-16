from base import *
from recruiter.candidate import Candidate


class Hackernews(Base):
    def getTitle(self):
        return self.dom.find("a", attrs={"class": "storylink"}).text

    def getCandidates(self):
        table = self.dom.find("table", attrs={"class": "comment-tree"})

        candidates = []
        for row in table.findAll("table"):
            candidate = {}

            # Grab span tag for Location meta.
            location = self.getMetaFromString(row.find("span", attrs={"class": "c00"}))
            if location:
                candidate[location["name"]] = location["value"]

            # Grab p tags for remaining metas.
            for line in row.findAll("p"):
                meta = self.getMetaFromString(line)
                if (meta):
                    candidate[meta["name"]] = meta["value"]

            if self.candidateMatchesFilters(candidate, self.params):
                candidates.append(candidate)

        return candidates

    @staticmethod
    def getNormalizedMetas():
        return {
            Candidate.META_EMAIL: [],
            Candidate.META_GITHUB: [],
            Candidate.META_LANGUAGES: [],
            Candidate.META_LINKEDIN: [],
            Candidate.META_LOCATION: [],
            Candidate.META_RELOCATE: [
                "relocation",
                "willing to relocate"
            ],
            Candidate.META_REMOTE: [],
            Candidate.META_RESUME: [
                "resume/cv",
                "r&#233;sum&#233;",
                "resume&#x2f;cv",
                "r&#233;sum&#233;&#x2f;cv"
            ],
            Candidate.META_SITE: [
                "blog",
                "portfolio",
                "website"
            ],
            Candidate.META_STACKOVERFLOW: [],
            Candidate.META_TECHNOLOGIES: [
                "frameworks",
                "tech",
                "tools"
            ]
        }

    @classmethod
    def isSupportedMeta(cls, meta):
        if len(meta) < 4:
            return False

        for name, aliases in cls.getNormalizedMetas().iteritems():
            if meta == name or meta in aliases:
                return True

        return False

    @classmethod
    def getNormalizedMeta(cls, meta):
        for name, aliases in cls.getNormalizedMetas().iteritems():
            if meta == name or meta in aliases:
                return name

        return meta

    @classmethod
    def getNormalizedMetaValue(cls, meta, value):
        if meta in [Candidate.META_RELOCATE, Candidate.META_REMOTE]:
            if "yes" in value.lower(): return "Yes"
            if "no" in value.lower() or "nope" in value.lower(): return "No"

        return value

    @classmethod
    def getMetaFromString(cls, string):
        if string is None:
            return False

        # Remove any HTML tags and rejoin matches as a string.
        meta = "".join(string.findAll(text=True))
        meta = meta.split(": ")

        if (len(meta) == 1):
            return False

        # Normalize the string and convert any UTF8 characters to html entities.
        name = meta[0].strip().lower().encode("ascii", "xmlcharrefreplace")

        if not cls.isSupportedMeta(name):
            return False

        name = cls.getNormalizedMeta(name)
        value = HTMLParser().unescape(meta[1].strip())

        return {
            "name": name,
            "value": cls.getNormalizedMetaValue(name, value)
        }

    @classmethod
    def candidateMatchesFilters(cls, candidate, filters):
        # Add candidate to list of candidates if it contains at least 2 supported metas.
        if (len(candidate) <= 1):
            return False

        matches = True
        for filter_meta, filter_values in filters.iteritems():
            if filter_meta not in candidate.keys():
                matches = False
                break

            filter_values = filter_values.split() if isinstance(filter_values, basestring) else filter_values

            for filter_value in filter_values:
                # Candidate must match one or more values for a given filter (but not all - OR not AND).
                if filter_value.lower() in candidate[filter_meta].lower():
                    matches = True
                    break
                else:
                    matches = False

            if not matches:
                # Set match if "location" filter fails but "relocate" filter is present.
                if (filter_meta == Candidate.META_LOCATION and
                        Candidate.META_RELOCATE in filters and
                        candidate[Candidate.META_RELOCATE] == "Yes"):
                    matches = True
                else:
                    break

        return matches
