from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class CareerJet(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Carrer Jet",
			"base_url": "https://www.careerjet.co.ke/search/jobs?",
			"domain": 'https://www.careerjet.co.ke',
			"method": "GET",
			"search_param": "s",
			"get_args": {"l": "Kenya"},
			"link_selector": 'article.job::attr(data-url)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["domain"]
		job["url"] = response.url
		job["jobTitle"] = self.clean_text(response.css('header h1::text').get())
		job["positionLevel"] = "N/A"
		job["positions"] = 1
		job["readvertised"] = "N/A"
		job["year"] = "2020"
		job["company"] = self.clean_text(response.css('p.company::text').get())
		job["technology"] = self.clean_text(response.css('header h1::text').get())
		job["industry"] = self.clean_text(response.css('header h1::text').get())
		job["country"] = "Kenya"
		self.get_header_details(response.css('header .details li *::text').getall(), job)
		self.get_tagged_details(response.css('header .tags li span::text').getall(), job)

		divs = response.css('.content *::text').getall()
		titles = response.xpath('//h3/text() | //strong /text() | //b/text()').getall()
		self.get_description(titles, divs, job)
		return job	

	def get_header_details(self, elements, job):
		if len(elements) > 2:
			job["town"] = self.clean_text(elements[2])
		if len(elements) > 4:
			job["employmentType"] = self.clean_text(elements[4])
		if len(elements) > 6:
			job["jobType"] = self.clean_text(elements[6])

	def get_tagged_details(self, elements, job):
		job["uploadDate"] = self.clean_text(elements[0])

	def get_description(self, titles, divs, job):
		divs = self.clean_page(divs)
		titles = self.clean_page(titles)
		text = self.clean_text(' '.join(divs))

		self.get_contacts(text, job)
		self.get_deadline(text, job)

		re_list = self.get_search_words(titles)

		self.regex_search(text, re_list, job)










		


