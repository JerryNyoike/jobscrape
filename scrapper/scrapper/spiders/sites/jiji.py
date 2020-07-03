from . import site
from .. import items
from re import search, IGNORE_CASE
from scrapy import Request


class Jiji(site.Site):
	"""Site class for https://www.ajiradigital.go.ke/home"""

	job = items.Job()

	def __init__(self):
		self.meta = {
			{
				name: "Jiji.ke",
				url: "https://jiji.co.ke/computing-and-it-jobs",
				domain: 'https://jiji.co.ke/',
				method: "GET",
				link_selector: 'a.b-list-advert::attr(href)'
			}
		}
		super().__init__(meta)

	def parse(self, response):
		job.ID = 1
		job.website = self.meta.domain
		job.url = response.url
		title = response.css('div.b-advert-title-inner::text').get()
	    job.jobTitle = title
	    job.positions = title
	    job.description = title
	    job.technology = title
	    job.uploadDate = response.css('time::text').get()
	    job.town = response.css('div.b-advert-info-statistics::text').get()
	    job.year = "2020"
	    job.contact = "N/A"
	    job.readvertised = "N/A"
		divs = response.css('div.b-render-attr::text').getall()
		get_details(divs)
		job.country = "Kenya"
		return job

	def get_details(self, divs):
		text = " ".join(divs)

	    company = search(r".Name(.*?)Job?", text, IGNORE_CASE)	
		if company:
			job.company = company.group(1)
			job.industry = company.group(1)
			text = sub(r".Name(.*?)Job?", company.group(1), text)

	    jobType = search(r".Type(.*?)Carrer?", text, IGNORE_CASE)	
		if jobType:
			job.jobType = jobType.group(1)
			job.employmentType = jobType.group(1)
			text = sub(r".Type(.*?)Carrer?", jobType.group(1), text)

		positionLevel = search(r".Level(.*?)Application?", text, IGNORE_CASE)
		if positionLevel:
			job.positionLevel = positionLevel.group(1)
			text = sub(r".Level(.*?)Application?", positionLevel.group(1), text)

		deadline = search(r".Deadline(.*?)Responsibilities?", text, IGNORE_CASE)
		if deadline:
			job.deadline = deadline.group(1)
			text = sub(r".Deadline(.*?)Responsibilities?", deadline.group(1), text)

		responsibilities = search(r".Responsibilities(.*?)Requirements?", text, IGNORE_CASE)
		if responsibilities:
			job.responsibilities = responsibilities.group(1)
			text = sub(r".Responsibilities(.*?)Requirements?", responsibilities.group(1), text)

		requirements = search(r".Skills(.*?)Minimum?", text, IGNORE_CASE)
		if requirements:
			job.requirements = requirements.group(1)
			job.skills = requirements.group(1)
			text = sub(r".Skills(.*?)Minimum?", requirements.group(1), text)

		qualifications = search(r".Requirements(.*?)Minimum?", text, IGNORE_CASE)
		if responsibilities:
			job.requirements = str(job.requirements + qualifications.group(1))
			text = sub(r".Responsibilities(.*?)Requirements?", responsibilities.group(1), text)

		salary = search(r".Salary(.*?)$", text, IGNORE_CASE)
		if salary:
			job.salary = salary.group(1)











		


