from . import site
from .. import items
from re import search, IGNORE_CASE
from scrapy import Request


class Jiji(site.Site):
	"""Site class for https://www.ajiradigital.go.ke/home"""

	job = items.Job()
	def __init__(self):
		self.meta = meta = {
			{
				name: "Site name",
				url: "site url",
				domain: 'site domain',
				method: "request method",
				link_selector: 'selector for follow link'
			}
		}
		super().__init__(meta)

	def parse(self, response):
		job = items.Job()
		job.ID = 1
		job.website = self.meta.domain
		job.url = response.url
	    job.jobTitle = response.css('selector::text').get()
	    job.jobType = response.css('selector::text').get()
	    job.positionLevel = response.css('selector::text').get()
	    job.positions = response.css('selector::text').get()
	    job.uploadDate = response.css('selector::text').get()
	    job.year = response.css('selector::text').get()
	   	job.deadline = response.css('selector::text').get()
	    job.town = response.css('selector::text').get()
	    job.contact = response.css('selector::text').get()
	    job.readvertised = response.css('selector::text').get()
	    job.salary = response.css('selector::text').get()
	    job.company = response.css('selector::text').get()
	    job.technology = response.css('selector::text').get()
	    job.description = response.css('selector::text').get()
	    job.employmentType = response.css('selector::text').get()
	    job.skills = response.css('selector::text').get()
	    job.industry = response.css('selector::text').get()
	   	job.responsibilities = response.css('selector::text').get()
	    job.requirements = response.css('selector::text').get()
	    job.country = response.css('selector::text').get()
		return job










		


