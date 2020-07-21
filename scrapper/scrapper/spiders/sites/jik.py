from . import site
from scrapper.items import Job
from lxml.etree import XPathEvalError
from urllib.parse import urlencode


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

        valid_position = lambda position: position if position != -1 else 0

        job = Job()

        title = response.xpath('//div[@class="job-title"]/text()').get()
        date = response.xpath('//div[@class="job-date"]/text()').get()
        year = date.split('.')[-1].strip()
        company = response.xpath('//div[@class="job-company"]/text()').get()
        location = response.xpath('//div[@class="job-location"]/text()').get()
        town = location.split(',')[0].strip()
        country = location.split(',')[-1].strip()
        description = self.clean_text(''.join(response.xpath('//div[@class="job-desc"]/p/text()').getall()))
        sumPos = valid_position(description.find('JOB SUMMARY'))
        respPos = valid_position(description.find('RESPONSIBILITIES'))
        skillPos = valid_position(description.find('REQUIRED SKILLS'))
        eduPos = valid_position(description.find('REQUIRED EDUCATION'))

        try:
            jobDesc = response.xpath('substring("{}", {}, {})'.format(description, sumPos, (respPos - sumPos))).get()
        except:
            jobDesc = ''
        try:
            skills = response.xpath('substring("{}", {}, {})'.format(description, skillPos, (eduPos-skillPos))).get()
        except:
            skills = ''
        try:
            education = response.xpath('substring("{}", {})'.format(description, eduPos)).get()
        except:
            education = ''
        try:
            reponsibilities = response.xpath('substring("{}", {}, {})'.format(description, respPos, (skillPos-respPos))).get()
        except:
            reponsibilities = ''
       

        contact = response.xpath('//div[@class="links"]/a[@class="view-job-link"]/@href').get()

        job["ID"] = 1
        job["website"] = self.meta["domain"]
        job["url"] = response.url
        job["jobTitle"] = title
        job["company"] = company
        job["jobType"] = "Fulltime"
        job["positionLevel"] = "N/A"
        job["uploadDate"] = date
        job["year"] = year
        job["deadline"] = "N/A"
        job["town"] = town
        job["country"] = country
        job["contact"] = contact
        job["readvertised"] = "N"
        job["technology"] = skills
        job["description"] = jobDesc
        job["employmentType"] = ''
        job["skills"] = skills
        job["industry"] = ''
        job["responsibilities"] = reponsibilities
        job["requirements"] = education
        job["country"] = country

        return job


    def createUrls(self, baseUrl, identifier, searchWords, params={}):
        ''' This function creates the search urls to be crawled by the spiders.
        baseUrl : the root of the website
        identifier : the name of the query parameter used by the site while performing a search
        searchWords : the words to search on the website
        returns the urls for the searches in a list which can then be used by start_urls or start_requests in a spider
        '''
        createQueryPairs = lambda keyword : {identifier: keyword}

        makeUrl = lambda keywordPair : baseUrl+(urlencode(keywordPair)).split('=')[-1]

        params = list(map(createQueryPairs, searchWords))

        return list(map(makeUrl, params))
