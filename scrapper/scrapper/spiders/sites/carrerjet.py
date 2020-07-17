from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class CareerJet(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Carrer Jet",
			"url": "https://www.careerjet.co.ke/search/jobs?",
			"domain": 'https://www.careerjet.co.ke/',
			"method": "GET",
			"search_param": "s",
			"get_params": {"l": "Kenya"},
			"link_selector": 'article.job::attr(data-url)'
		}
	
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["domain"]
		job["url"] = response.url
		job["jobTitle"] = self.clean_text(response.css('header h1::text').get())
		job["positionLevel"] = response.css('selector::text').get()
		job["positions"] = response.css('selector::text').get()
		job["year"] = response.css('selector::text').get()
		job["deadline"] = response.css('selector::text').get()
		job["contact"] = response.css('selector::text').get()
		job["readvertised"] = response.css('selector::text').get()
		job["salary"] = response.css('selector::text').get()
		job["company"] = response.css('selector::text').get()
		job["technology"] = response.css('selector::text').get()
		job["description"] = response.css('selector::text').get()
		job["skills"] = response.css('selector::text').get()
		job["industry"] = response.css('selector::text').get()
		job["responsibilities"] = response.css('selector::text').get()
		job["requirements"] = response.css('selector::text').get()
		job["country"] = "Kenya"
		self.get_header_details(response.css('header .details li *::text').getall(), job)
		self.get_tagged_details(response.css('header .tags li span::text').getall(), job)
		self.get_description(response.css('.content *::text').getall(), job)
		return job	

	def get_header_details(self, elements, job):
		job["town"] = self.clean_text(elements[2])
		job["employmentType"] = self.clean_text(elements[4])
		job["jobType"] = self.clean_text(elements[6])

	def get_tagged_details(self, elements, job):
		job["uploadDate"] = self.clean_text(elements[0])

	def get_description(self, divs, job):
		divs = self.clean_page(divs)
		text = self.clean_text(' '.join(divs))

		re_list = [
			{
				"re": r".?Job description(.*?)Requirements?",
				"fields": [""]
			}
		]

		self.regex_search(text, re_list, job)










		


