from . import site
from scrapper.items import Job
from lxml.etree import XPathEvalError
from urllib.parse import urlencode


class CareerPoint(site.Site):
    '''
    Site class for Careerpoint
    '''

    def __init__(self):
        self.meta = {
            "name": "Career Point",
            "base_url": "https://careerpointkenya.co.ke/?",
            "domain": "https://careerpointkenya.co.ke/",
            "method": "GET",
            "search_param": "s",
            "link_selector": "h2.entry-title a::attr(href)",
            "next_page_selector": "div.pagination a.pagination-next::attr(href)",
        }
        super().__init__(self.meta)


    def parse(self, response):
        job = Job()

        desc = response.xpath('//*[contains(text(), "Description")]/following::p[1]/text() | //div[@id="carrerbox"]/descendant-or-self::div[@class="wpb_wrapper"]/p/strong/span[contains(text(), "Job description")]/following::p[1]/text()').get()
        resp = ''.join(response.xpath('//*[contains(text(), "Responsibilities")]/following::ul[1]/li/text() | //div[@class="jobs-subheading"]/span/strong[contains(text(), "Responsibilities")]/ancestor::div/following-sibling::div/ul[1]/li/div/p/text()').getall())
        qualifications = ''.join(response.xpath('//*[contains(text(), "Responsibilities")]/following::ul[2]/li/text() | //div[@class="jobs-subheading"]/span/strong[contains(text(), "Responsibilities")]/ancestor::div/following-sibling::div/ul[1]/li/div/p/text()').getall())
        if qualifications.find("Degree") == -1:
            education = "N/A"
        else:
            education = qualifications[qualifications.find("Degree"):qualifications.find(".")]

        contact = response.xpath('//p/strong[contains(text(), "@")]/text() | //p/span/strong[contains(text(), "How to Apply")]/following::p[1]/span/a/@href').get()
        title = response.xpath('//h1[contains(@class, "entry-title")]/text()').get()
        position = response.xpath('//div[@class="wpb_wrapper"]/p[contains(text(), "Position")]/text()').get()
        if position is not None:
            position = position.split(':')[-1].strip()
        location = response.xpath('//div[@class="wpb_wrapper"]/p[contains(text(), "Location")]/text()').get()
        if location is not None:
            location = location.split(':')[-1].strip()
        industry = response.xpath('//div[@class="row"]/p[1]/text()').get()


        job["ID"] = 1
        job["website"] = self.meta["domain"]
        job["url"] = response.url
        job["jobTitle"] = title
        job["company"] = title.split('Job')[-1]
        job["jobType"] = "Fulltime"
        job["positionLevel"] = position
        job["uploadDate"] = "N/A"
        job["year"] = "2020"
        job["deadline"] = "N/A"
        job["town"] = location
        job["country"] = "Kenya"
        job["contact"] = contact
        job["readvertised"] = "N/A"
        job["technology"] = resp
        job["description"] = desc
        job["employmentType"] = "Fulltime"
        job["skills"] = qualifications
        job["industry"] = industry
        job["responsibilities"] = resp
        job["requirements"] = education
        job["country"] = "Kenya"

        return job