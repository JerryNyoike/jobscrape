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
        job["ID"] = 1
        job["website"]= self.meta["domain"]
        job["url"] = response.url
        job["readvertised"] = "N/A"
        job["year"] = "2020"
        job["positionLevel"] = "N/A"
        job["positions"] = 1
        job["jobTitle"] = response.xpath('//div[@class="flex-full"]/h3[contains(@class, "mt-500")]/text()').get()
        location = response.xpath('//div[contains(@class, "mb-500")]/text()').get()
        if location is not None:
            job["country"] = location.split(',')[-1].strip()
            job["town"] = location.split(',')[0].strip()
        job["company"] = response.xpath('//div[contains(@class, "mb-500")]/a/text()').get()
        job["salary"] = response.xpath('//div[@class="flex-full"]/p[1]/span[contains(text(), "Salary")]/following::span/text()').get()
        employmentType = response.xpath('//div[@class="flex-full"]/p[1]/text()').getall()
        if len(employmentType) > 0:
            job["employmentType"] = employmentType[1].strip()
            job["jobType"] = employmentType[1].strip()

        divs = response.css('div.row-flex div.border-grey-sm *::text').getall()
        titles = response.xpath('//h4/text() | //strong /text() | //b/text()').getall()
        self.get_description(titles, divs, job)

        return job


    def extract_links(self, response):
        ''' 
        Make a request to the API and pick out the job urls
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
        urls = super().createUrls(baseUrl, identifier, searchWords, params)
        add_page = lambda link : link + '&' + urlencode(params, quote_via=quote)
        final_urls = list(map(add_page, urls))
        return final_urls

    def get_description(self, titles, divs, job):
        divs = self.clean_page(divs)
        titles = self.clean_page(titles)
        text = self.clean_text(' '.join(divs))

        self.get_contacts(text, job)
        self.get_deadline(text, job)

        re_list = self.get_search_words(titles)

        self.regex_search(text, re_list, job)