from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class BestJobs(site.Site):
	"""Site class for https://www.bestjobskenya.com"""

	
	def __init__(self):
		self.meta = {
			"name": "Best Jobs Kenya",
			"base_url": "https://www.bestjobskenya.com/job-of-design?",
			"domain": 'https://www.bestjobskenya.com',
			"method": "GET",
			"search_param": "q",
			"link_selector": 'a.js-o-link::attr(href)',
			"next_page_selector": '.siguiente a::attr(href)'
		}
		super().__init__(self.meta)

	def parse(self, response):
		job = Job()

		job["website"]= self.meta["domain"]
		job["url"] = response.url
		jobTitle = self.clean_text(response.css('h1::text').get())
		job["jobTitle"] = jobTitle
		job["technology"] = jobTitle
		job["industry"] = jobTitle
		job["positionLevel"] = "N/A"
		job["year"] = "2020"
		job["readvertised"] = "N/A"
		job["company"] = self.clean_text(response.css('h2::text').get())
		job["skills"] = response.css('selector::text').get()
		job["responsibilities"] = "N/A"
		job["country"] = "Kenya"

		self.get_type(response.css('.box_r *::text').getall(), job)
		self.get_header_details(response.css('header span::text').getall(), job)
		self.get_description(response.css('.detalle_oferta ul *::text').getall(), job)
		return job

	def get_header_details(self, spans, job):
		job["salary"] = self.clean_text(spans[0])
		if len(spans) > 1:
			job["town"] = self.clean_text(spans[1])
		if len(spans) > 2:
			job["uploadDate"] = self.clean_text(spans[2])

	def get_type(self, p, job):
		p = self.clean_page(p)
		text = self.clean_text(' '.join(p))
		search_result = search(r".?Type of contract(.*?)", text, IGNORECASE)
		if search_result:
			job["jobType"] = search_result.group(1)
			job["employmentType"] = search_result.group(1)

	def get_description(self, divs, job):
		divs = self.clean_page(divs)
		text = " ".join(divs)

		re_list = [
			{
				"re": r".?Description(.*?)QUALIFICATIONS?",
				"fields": ["description"]
			},
			{
				"re": r".?QUALIFICATIONS(.*?)HOW TO APPLY?",
				"fields": ["skills"]
			},
			{
				"re": r".?Hiring manager on(.*?)strictly?",
				"fields": ["contact"]
			},
			{
				"re": r".?Number of vacancies(.*?)Requirements?",
				"fields": ["positions"]
			},
			{
				"re": r".?Requirements(.*?)$",
				"fields": ["requirements", "skills"]
			}
		]

		self.get_contacts(text, job)
		self.get_deadline(text, job)
		
		self.regex_search(text, re_list, job)










		


