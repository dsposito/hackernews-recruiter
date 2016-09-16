from base import *


class Google(Base):
    def getFirstResultUrl(self):
        results = self.dom.find("div", attrs={"id": "search"})
        result = results.find("cite")

        return result.text
