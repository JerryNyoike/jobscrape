from . import site
from scrapper.item import Job


class Fuzu(site.Site):
    '''
    Site class for Fuzu website
    '''
    def __init__(self):
        self.meta = {
                "name": "Fuzu",
                "base_url": "https://www.fuzu.com/jobs/search?",
                "domain": "https://www.fuzu.com/",
                "method": "GET",
                "searchParam": "searchTerm",
                "link_selector": "",
                "next_page_selector": ""
                }
        super().__init__(self.meta)


    def parse(self, response):
        job = Job()

        return job
