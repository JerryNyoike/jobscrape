from . import site
from scrapper.items import Job


class CoopStaffing(site.Site):
    """
    A class for corporate staffing site
    """
    def __init__(self):
        self.meta = {
            "name": "Corporate Staffing",
            "base_url": "https://www.corporatestaffing.co.ke/?",
            "domain": "https://www.corporatestaffing.co.ke",
            "method": "GET",
            "search_param": "s",
            "link_selector": "a.entry-title-link::attr(href)",
            "next_page_selector": "div.pagination-next a::attr(href)"
            }
        super().__init__(self.meta)

    def parse(self, response):
        job = Job()

        jobContent = response.xpath('//main[@class="content"]/article[contains(@class, "job_posting")]')
        jobDetails = jobContent.xpath('//div[@class="entry-content"]')
        jobMeta = response.xpath('//footer/p[@class="entry-meta"]')
        title = jobContent.xpath('//header[@class="entry-header"]/h1[@class="entry-title"]/text()').get()
        uploadTime = jobContent.xpath('//header[@class="entry-header"]/p/time/text()').get()
        if uploadTime:
            year = uploadTime.split(" ")[2]
        else:
            year = "N/A"
        jobType = jobMeta.xpath('//span[contains(@class, "wsm-categories")]/a[1]/text()').get()

        description = ''.join(jobDetails.xpath('//p/strong[contains(text(), "Title")]/ancestor::p/preceding-sibling::p/text()').getall())
        salary = jobDetails.xpath('//p/strong[contains(text(), "Gross Salary")]/ancestor::p/text()').get()
        if salary:
            salary = salary.strip()
        else:
            salary = "N/A"

        town = jobDetails.xpath('//p/strong[contains(text(), "Location")]/ancestor::p/text()').get()
        if town is not None:
            town = town.strip()
        else:
            town = "N/A"

        skills = ''.join(jobDetails.xpath('//p/span/strong[contains(text(), "Qualifications")]/ancestor::p/following-sibling::ul[1]/li/text()').getall())
        responsibilities = ''.join(jobDetails.xpath('//p/span/strong[contains(text(), "Responsibilities")]/ancestor::p/following-sibling::ul[1]/li/text()').getall())
        contact = jobDetails.xpath('//p/span/strong[contains(text(), "How to Apply")]/ancestor::p/span/strong[contains(text(), "@")]/text()').get()
        company = jobMeta.xpath('//span[last()]/a/text()').get()
        applicationDetails = jobDetails.xpath('//p/span/strong[contains(text(), "How to Apply")]/ancestor::p/text()').getall()
        if applicationDetails:
            deadline = ''.join([applicationDetails[-2], applicationDetails[-1]]).strip()
        else:
            deadline = "N/A"
        industry = jobMeta.xpath('//p/span[@class="entry-tags"]/a/text()').get()
        country = 'Kenya'
        requirements = 'N/A'
        positionLevel = 'N/A'
        technology = jobDetails.xpath('//p[3]/strong/text()').get()

        job["ID"] = 1
        job["website"] = self.meta["name"]
        job["url"] = response.url
        job["jobTitle"] = title
        job["jobType"] = jobType
        job["positionLevel"] = "N/A"
        job["positions"] = 1
        job["uploadDate"] = uploadTime
        job["year"] = year
        job["deadline"] = deadline
        job["town"] = town
        job["contact"] = contact
        job["readvertised"] = "NO"
        job["salary"] = salary
        job["company"] = company
        job["technology"] = technology
        job["description"] = description
        job["employmentType"] = jobType
        job["skills"] = skills
        job["industry"] = industry
        job["responsibilities"] = responsibilities
        job["requirements"] = requirements
        job["country"] = country

        return job
