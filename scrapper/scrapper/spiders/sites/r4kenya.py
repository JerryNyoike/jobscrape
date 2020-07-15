from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class R4kenya(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "R4 Kenya",
			"base_url": "https://r4kenya.com/jobs/?",
			"domain": 'https://r4kenya.com',
			"method": "GET",
			"search_param": "q",
			"get_args": {"l": "Kenya"},
			"link_selector": 'a.is-block::attr(href)'
		}
		self.search_words = [
			{
				"fields": ["description"],
				"titles": "Description, Details, The Role, Overview"
			},
			{
				"fields": ["skills"],
				"titles": "Qualifications, Nice to have, Competencies, Skills, Experience, Requirements"
			},
			{
				"fields": ["responsibilities"],
				"titles": "Responsibilities, Tasks"
			}
		]
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["domain"]
		job["url"] = response.url
		job["jobTitle"] = response.css('header h1.title::text').get()
		job["positionLevel"] = response.css('header h1.title::text').get()
		job["positions"] = 1
		job["uploadDate"] = response.css('time.time::attr(datetime)').get()
		job["deadline"] = response.css('selector::text').get()
		job["readvertised"] = "N/A"
		job["salary"] = "N/A"
		job["technology"] = response.css('header h1.title::text').get()
		
		job["country"] = "Kenya"
		self.get_header_details(response.css('article header span::text').getall(), job)

		titles = response.css('.content strong::text').getall()
		divs = response.css('.content *::text').getall()
		self.get_description(titles, divs, job)
		return job	

	def get_header_details(self, spans, job):
		if spans:
			job["company"] = spans[0]
			job["industry"] = spans[0]
			if len(spans) > 1:
				job["town"] = spans[1]
			if len(spans) > 2:
				job["jobType"] = spans[2]
				job["employmentType"] = spans[2]

	def get_description(self, titles, divs, job):
		divs = self.clean_page(divs)
		titles = self.clean_page(titles)
		text = self.clean_text(' '.join(divs))

		re_list = [
			{
				"re": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
				"fields": ["contact"]
			}
		]

		deadline_search = search(r"Deadline:(.+?)(\d{4})", text, IGNORECASE)
		if deadline_search:
			job["deadline"] = deadline_search.group(1) + deadline_search.group(2)
			job["year"] = deadline_search.group(2)

		self.get_search_words(titles, re_list)

		self.regex_search(text, re_list, job)