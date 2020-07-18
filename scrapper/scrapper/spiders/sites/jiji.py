from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class Jiji(site.Site):
	"""Site class for https://www.jiji.co.ke/"""

	def __init__(self):
		self.meta = {
			"name": "Jiji.ke",
			"base_url": "https://jiji.co.ke/jobs?",
			"domain": 'https://jiji.co.ke',
			"method": "GET",
			"search_param": "query",
			"link_selector": 'a.b-list-advert__item-image::attr(href)'
		}
		
		super().__init__(self.meta)

	def parse(self, response):
		job = Job()
		job["ID"]= 1
		job["website"] = self.meta["domain"]
		job["url"] = response.url
		title = self.clean_text(response.css('.b-advert-title-inner::text').get())
		job["jobTitle"] = title
		job["positions"] = 1
		job["description"] = title
		job["technology"] = title
		job["uploadDate"] = self.clean_text(response.css('time::text').get())
		job["town"] = self.clean_text(response.css('.b-advert-info-statistics::text').get())
		job["year"] = "2020"
		job["contact"] = "N/A"
		job["readvertised"] = "N/A"
		job["country"] = "Kenya"
		divs = response.css(".b-advert-attributes *::text").getall()
		self.get_details(divs, job)
		return job

	def get_details(self, divs, job):
		divs = self.clean_page(divs)
		text = " ".join(divs)

		re_list = [
			{
				"re": r".?Name(.*?)Job?",
				"fields": ["company", "industry"]
			},
			{
				"re": r".?Type(.*?)Carrer?",
				"fields": ["jobType", "employmentType"]
			},
			{
				"re": r".?Level(.*?)Application?",
				"fields": ["positionLevel"]
			},
			{
				"re": r".?Deadline(.*?)Responsibilities?",
				"fields": ["deadline"]
			},
			{
				"re": r".?Responsibilities(.*?)Requirements?",
				"fields": ["responsibilities"]
			},
			{
				"re": r".?Skills(.*?)Minimum?",
				"fields": ["requirements", "skills"]
			},
			{
				"re": r".?Requirements(.*?)Minimum?",
				"fields": ["skills"]
			},
			{
				"re": r".?Salary(.{2,30}).?",
				"fields": ["salary"]
			}
		]

		self.get_contacts(text, job)
		self.get_deadline(text, job)

		self.regex_search(text, re_list, job)