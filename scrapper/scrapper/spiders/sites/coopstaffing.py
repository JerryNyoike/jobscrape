import site
from scrapy.Loaders import ItemLoader
from scrapper.items import Job
from re import search, IGNORECASE


class Sokoso(site.Site):
    """
    A class for sokoso site
    """
    def __init__(self):
        sokoso_meta = [{
            "name": "Sokoso",
            "base_url": "https://www.sokoso.co.ke/jobs/search?",
            "domain": "https://www.sokoso.co.ke/jobs/",
            "method": "GET",
            "search_param": "q"
            "link_selector": "",
            }]
        super.meta(sokoso_meta)

    def parse(self, response):
        pass

    def 
