from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class BrighterMonday(site.Site):
	"""Site class for https://www.brightermonday.co.ke/"""

	def __init__(self):
		self.meta = {
			"name": "Brighter Monday",
			"base_url": "https://www.brightermonday.co.ke/jobs?",
			"domain": 'https://www.brightermonday.co.ke',
			"method": "GET",
			"search_param": "q",
			"link_selector": '.search-result__job-title::attr(href)',
			"next_page_selector": 'ul.pagination li:last-child a::attr(href)'
		}
		super().__init__(self.meta)

	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"] = self.meta["name"]
		job["url"] = response.url
		job["jobTitle"] = self.clean_text(response.css('.job-header__title::text').get())
		job["positions"] = 1
		jobType = self.clean_text(response.css('.job-header__work-type::text').get())
		job["jobType"] = jobType
		job["employmentType"] = jobType
		job["year"] = "2020"
		job["readvertised"] = "N/A"
		job["salary"] = self.clean_text(response.css('.job-header__salary::text').get())
		job["country"] = "Kenya"
		self.get_town(response.css('.job-header__location *::text').getall(), job)
		self.get_company(response.css('h2 *::text').getall(), job)
		self.get_description(response.css('.job__details *::text').getall(), job)
		return job

	def get_company(self, h2s, job):
		if h2s:
			job["company"] = self.clean_text(h2s[0])
			if len(h2s) > 1:
				job["technology"] = self.clean_text(h2s[1])

	def get_town(self, divs, job):
		if divs:
			job["town"] = self.clean_text(divs[0])
			if len(divs) > 1:
				job["industry"] = self.clean_text(divs[1])

	def get_description(self, divs, job):
		divs = self.clean_page(divs)
		text = " ".join(divs)

		re_list = [
			{
				"re": r".?Job Summary(.*?)Responsibilities?",
				"fields": ["description"]
			},
			{
				"re": r".?Qualification(.*?)Experience?",
				"fields": ["skills"]
			},
			{
				"re": r".?Level:(.*?)Experience?",
				"fields": ["positionLevel"]
			},
			{
				"re": r".?Responsibilities:(.*?)Requirements?",
				"fields": ["responsibilities"]
			},
			{
				"re": r".?Requirements(.*?)$",
				"fields": ["requirements", "skills"]
			}
		]

		self.get_contacts(text, job)
		self.get_deadline(text, job)

		self.regex_search(text, re_list, job)
