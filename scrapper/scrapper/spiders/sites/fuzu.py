from . import site
from scrapper.items import Job
from scrapy import Request
import json
from urllib.parse import urlencode, quote


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
                "next_page_selector": "",
                "api": "https://www.fuzu.com/api/jobs?"
                }
        super().__init__(self.meta)


    def parse(self, response):
        job = Job()

        return job


    def extract_links(self, response):
        ''' Make a request to the API and pick out the job urls
        '''
        get_urls = lambda data_item : data_item.get("url")
        data = json.loads(response.body)
        details = data.get("jobs_api_cacher")
        if len(details) == 0:
            return None

        urls = list(map(get_urls, details))
        return urls

    def next_page_url(self, url):
        return url.replace(url[-1], str(int(url[-1])+1))

    def createUrls(self, baseUrl, identifier, searchWords, params):
        urls = super().createUrls(baseUrl, identifier, searchWords)
        add_page = lambda link : link + '&' + urlencode(params, quote_via=quote)
        final_urls = list(map(add_page, urls))
        return final_urls
