from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser


class Base(object):
    dom = None
    text = None
    params = {}

    def __init__(self, text, params={}):
        self.dom = BeautifulSoup(text)
        self.text = text
        self.params = params
