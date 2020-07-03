from . import site
from .. import items
from re import search, sub, IGNORE_CASE
from scrapy import Request


class BrighterMonday(site.Site):
	"""Site class for https://www.ajiradigital.go.ke/home"""

	job = items.Job()

	def __init__(self):
		self.meta = meta = {
			{
				name: "Brighter Monday",
				url: "https://www.brightermonday.co.ke/jobs/software-data?industry[]=it-telecoms",
				domain: 'https://www.brightermonday.co.ke/',
				method: "GET",
				link_selector: 'a.search-result__job-title::attr(href)'
			}
		}
		super().__init__(meta)

	def parse(self, response):
		job.ID = 1
		job.website = self.meta.domain
		job.url = response.url
		title = response.css('h1.job-header__title::text').get()
		job.jobTitle = title
		job.positions = title
		jobType = response.css('span.job-header__work-type::text').get()
		job.jobType = jobType
		job.employmentType = jobType
		job.industry = jobType
		job.uploadDate = "N/A"
		job.year = "N/A"
		job.deadline = "N/A"
		job.town = response.css('span.job-header__location a:nth-child()::text').get()
		job.contact = "N/A"
		job.readvertised = "N/A"
		job.salary = response.css('div.job-header__salary').get()
		job.country = "Kenya"
		get_company(response.css('h2::text').getall())
		get_description(response.css("div.customer-card__content-segment::text").getall())
		return job

	def get_company(self, h2s):
		job.company = h2s[0]
		job.technology = h2s[1]

	def get_description(self, divs):
		text = ' '.join(divs)

		description = search(r".Job brief(.*?)Responsibilities?", text, IGNORE_CASE)
		if description:
			job.description = description.group(1)
			text = sub(r".Job brief(.*?)Responsibilities?", description.group(1), text)

		qualification = search(r".Qualification(.*?)Experience?", text, IGNORE_CASE)
		if qualification:
			jop.qualification = qualification.group(1)
			job.requirements = qualification.group(1)

		positionLevel = search(r".Level:(.*?)Experience?", text, IGNORE_CASE)
		if positionLevel:
			jop.positionLevel = positionLevel.group(1)
			text = sub(r".Level:(.*?)Experience?", positionLevel.group(1), text)

		responsibilities = search(r".Responsibilities:(.*?)Requirements?", text, IGNORE_CASE)
		if responsibilities:
			jop.responsibilities = responsibilities.group(1)
			text = sub(r".Responsibilities:(.*?)Requirements?", responsibilities.group(1), text)

		requirements = search(r".Requirements(.*?)$", text, IGNORE_CASE)
		if requirements:
			jop.requirements = str(job.requirements + requirements.group(1))
			job.skills = requirements.group(1)










		


