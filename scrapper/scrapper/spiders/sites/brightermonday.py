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
		job["website"] = self.meta["domain"]
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

		contact_search = search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text, IGNORECASE)
		if contact_search:
			job["contact"] = contact_search.group(0)	

		deadline_search = search(r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})", text, IGNORECASE)
		if deadline_search:
			job["deadline"] = deadline_search.group(0)
			job["uploadDate"] = deadline_search.group(0)

		self.regex_search(text, re_list, job)
