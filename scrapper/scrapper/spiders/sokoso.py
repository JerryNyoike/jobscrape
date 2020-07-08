import site
from scrapper.items import Job
from re import search, IGNORECASE


class Sokoso(site.Site):
    """
    A class for sokoso site
    """
    def __init__(self):
        sokoso_meta = [{
            "name": "Sokoso",
            "url": "",
            "domain": "",
            "method": "",
            "link_selector": "",
            }]
        super.meta(sokoso_meta)

    def parse(self, response):
        pass

    def 
