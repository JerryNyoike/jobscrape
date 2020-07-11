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

        super().__init__(self.meta)


    def parse(self, response):
        job = Job()

        title = response.xpath('//div[@class="job-title"]/text()').get()
        date = response.xpath('//div[@class="job-date"]/text()').get()
        company = response.xpath('//div[@class="job-company"]/text()').get()
        location = response.xpath('//div[@class="job-location"]/text()').get()
        description = ''.join(response.xpath('//div[@class="job-desc"]/p/text()').getall())
