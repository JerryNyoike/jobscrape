from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class BrighterMonday(site.Site):
	"""Site class for https://www.ajiradigital.go.ke/home"""

	def __init__(self):
		self.meta = [
			{
				"name": "Brighter Monday",
				"url": "https://www.brightermonday.co.ke/jobs/software-data?industry[]=it-telecoms",
				"domain": 'https://www.brightermonday.co.ke/',
				"method": "GET",
				"link_selector": '.search-result__job-title::attr(href)'
			}
		]
		super().__init__(self.meta)

	def parse(self, response):
		job = Job()
		job.ID = 1
		job.website = self.meta.domain
		job.url = response.url
		job.jobTitle = response.css('.job-header__title::text').get()
		job.positions = 1
		jobType = response.css('.job-header__work-type::text').get()
		job.jobType = jobType
		job.employmentType = jobType
		job.uploadDate = "N/A"
		job.year = "N/A"
		job.deadline = "N/A"
		job.contact = "N/A"
		job.readvertised = "N/A"
		job.salary = response.css('.job-header__salary').get()
		job.country = "Kenya"
		get_town(response.css('.job-header__location *::text').getall(), job)
		get_company(response.css('h2 *::text').getall(), job)
		get_description(response.css('.job__details *::text').getall(), job)
		return job

	def get_company(self, h2s, job):
		job.company = h2s[0]
		job.technology = h2s[1]

	def get_town(self, divs, job):
		job.town = divs[0]
		job.industry = divs[1]

	def get_description(self, divs, job):
		text = self.clean_soup(' '.join(divs))

		description = search(r".?Job Summary(.*?)Responsibilities?", text, IGNORE_CASE)
		if description:
			job.description = description.group(1)
			text = text.replace(description.group(1), '')

		qualification = search(r".?Qualification(.*?)Experience?", text, IGNORE_CASE)
		if qualification:
			jop.qualification = qualification.group(1)
			job.requirements = qualification.group(1)
			text = text.replace(qualification.group(1), '')

		positionLevel = search(r".?Level:(.*?)Experience?", text, IGNORE_CASE)
		if positionLevel:
			jop.positionLevel = positionLevel.group(1)
			text = text.replace(positionLevel.group(1), '')

		responsibilities = search(r".?Responsibilities:(.*?)Requirements?", text, IGNORE_CASE)
		if responsibilities:
			jop.responsibilities = responsibilities.group(1)
			text = text.replace(responsibilities.group(1), '')

		requirements = search(r".?Requirements(.*?)$", text, IGNORE_CASE)
		if requirements:
			jop.requirements = str(job.requirements + requirements.group(1))
			job.skills = requirements.group(1)










		


