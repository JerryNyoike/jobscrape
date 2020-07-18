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

		contact_search = search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text, IGNORECASE)
		if contact_search:
			job["contact"] = contact_search.group(0)	

		deadline_search = search(r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})", text, IGNORECASE)
		if deadline_search:
			job["deadline"] = deadline_search.group(0)

		self.regex_search(text, re_list, job)