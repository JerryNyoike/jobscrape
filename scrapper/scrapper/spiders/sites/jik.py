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
        year = date.split('.')[-1].strip()
        company = response.xpath('//div[@class="job-company"]/text()').get()
        location = response.xpath('//div[@class="job-location"]/text()').get()
        town = location.split(',')[0].strip()
        country = location.split(',')[-1].strip()
        description = ''.join(response.xpath('//div[@class="job-desc"]/p/text()').getall())
        sumPos = description.find('JOB SUMMARY')
        respPos = description.find('RESPONSIBILITIES')
        skillPos = description.find('REQUIRED SKILLS')
        eduPos = description.find('REQUIRED EDUCATION')

        jobDesc = response.xpath('substring("{}", {}, {})'.format(description, sumPos, respPos)).get()
        reponsibilities = response.xpath('substring("{}", {}, {})'.format(description, respPos, skillPos)).get()
        skills = response.xpath('substring("{}", {}, {})'.format(description, skillPos, eduPos)).get()
        education = response.xpath('substring("{}", {})'.format(description, eduPos)).get()

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
        job["qualification"] = education
        job["industry"] = ''
        job["responsibilities"] = reponsibilities
        job["requirements"] = education
        job["country"] = country

        return job
