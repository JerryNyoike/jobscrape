from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class Kenyads(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Kenya Ads",
			"base_url": "https://www.kenyads.com/listings.php?",
			"domain": 'https://www.kenyads.com/',
			"method": "GET",
			"search_param": "industry",
			"link_selector": 'div.card-body h4 a::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["domain"]
		job["url"] = response.url
		job["jobTitle"] = response.css('#postJob h2::text').get()
		job["jobType"] = response.css('selector::text').get()
		job["positionLevel"] = response.css('#postJob h2::text').get()
		job["positions"] = response.css('selector::text').get()
		job["uploadDate"] = response.css('selector::text').get()
		job["year"] = response.css('selector::text').get()
		job["deadline"] = response.css('selector::text').get()
		job["town"] = response.css('selector::text').get()
		job["contact"] = response.css('selector::text').get()
		job["readvertised"] = response.css('selector::text').get()
		job["salary"] = response.css('selector::text').get()
		job["company"] = response.css('selector::text').get()
		job["technology"] = response.css('selector::text').get()
		job["description"] = response.css('selector::text').get()
		job["employmentType"] = response.css('selector::text').get()
		job["skills"] = response.css('selector::text').get()
		job["industry"] = response.css('selector::text').get()
		job["responsibilities"] = response.css('selector::text').get()
		job["requirements"] = response.css('selector::text').get()
		job["country"] = "Kenya"
		
		self.get_header_details(response.css('article header span::text').getall(), job)

		titles = response.xpath('//h3/text() | //strong /text() | //b/text()').getall()
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
		
		deadline_search = search(r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})", text, IGNORECASE)
		if deadline_search:
			job["deadline"] = deadline_search.group(0)

		contact_search = search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text, IGNORECASE)
		if contact_search:
			job["contact"] = contact_search.group(0)

		re_list = self.get_search_words(titles, re_list)

		self.regex_search(text, re_list, job)