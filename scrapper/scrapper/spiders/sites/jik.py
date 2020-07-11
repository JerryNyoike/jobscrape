from . import site
from scrapper.items import Job


class Jik(site.Site):
    '''
    Site class for jobs in kenya
    '''

    def __init__(self):
        self.meta = {
                "name": "Jobs in Kenya",
                "base_url": "https://jobsinkenya.net/Kenya",
                "domain": "https://jobsinkenya.net",
                "method": "GET",
                "search_param": "",
                "link_selector": "div.jobs-container div.job-wrapper a.job::attr(href)",
                "next_page_selector": "div.pagination a::attr(href)"
                }

