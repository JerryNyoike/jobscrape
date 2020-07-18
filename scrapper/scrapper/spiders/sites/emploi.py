from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class Emploi(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Emploi",
			"base_url": "https://www.emploi.co/vacancies/search?",
			"domain": 'https://www.emploi.co',
			"method": "GET",
			"search_param": "q",
			"link_selector": 'div.card-body h4 a::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["domain"]
		job["url"] = response.url
		job["jobTitle"] = response.css('#postJob h2::text').get()
		job["positions"] = 1
		job["uploadDate"] = response.xpath("//span[contains(text(), 'Posted')]/*/text()").get()
		job["year"] = "2020"
		job["deadline"] = "N/A"
		job["town"] = self.clean_text(' '.join(response.css('div.card-body div.pb-3 p::text').getall()))
		job["readvertised"] = "N/A"
		job["salary"] = "Login to view salary"
		job["country"] = "Kenya"

		self.get_header_details(response.css('#job-description div.card-body div.pb-3 a *::text').getall(), job)
 
		divs = response.css('#job-description div.card-body *::text').getall()
		titles = response.xpath('//h5/text() | //strong /text() | //b/text()').getall()
		self.get_description(titles, divs, job)
		return job	

	def get_header_details(self, spans, job):
		spans = self.clean_page(spans)
		spans = self.drop_empty_fields(spans)
		if spans:
			job["company"] = spans[0]
			if len(spans) > 2:
				job["jobType"] = spans[2]
				job["employmentType"] = spans[2]
			if len(spans) > 3:
				if spans[2] == 'Featured':
					job["jobType"] = spans[3]
					job["employmentType"] = spans[3]
					job["technology"] = spans[5]
					job["industry"] = spans[5]
					job["positionLevel"] = spans[5]
				else:
					job["technology"] = spans[3]
					job["industry"] = spans[3]
					job["positionLevel"] = spans[3]



	def get_description(self, titles, divs, job):
		divs = self.clean_page(divs)
		titles = self.clean_page(titles)
		text = self.clean_text(' '.join(divs))

		contact_search = search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text, IGNORECASE)
		if contact_search:
			job["contact"] = contact_search.group(0)

		deadline_search = search(r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})", text, IGNORECASE)
		if deadline_search:
			job["deadline"] = deadline_search.group(0)

		re_list = self.get_search_words(titles)

		self.regex_search(text, re_list, job)










		

