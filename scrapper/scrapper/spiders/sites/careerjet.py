from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class CareerJet(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Carrer Jet",
			"base_url": "https://www.careerjet.co.ke/search/jobs?",
			"domain": 'https://www.careerjet.co.ke/',
			"method": "GET",
			"search_param": "s",
			"get_args": {"l": "Kenya"},
			"link_selector": 'article.job::attr(data-url)'
		}
		self.search_words = [
			{
				"fields": ["description"],
				"titles": "Description, Summary, Details, Opportunity, The Role, Overview"
			},
			{
				"fields": ["requirements", "skills"],
				"titles": "Qualifications, Candidate Profile, Competencies, Skills, Experience, Requirements"
			},
			{
				"fields": ["responsibilities"],
				"titles": "Responsibilities, Tasks, Duties"
			},
			{
				"fields": ["salary"],
				"titles": "Salary, Remuneration"
			}
		]
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
		job["company"] = self.clean_text(response.css('p.company::text').get())
		job["technology"] = self.clean_text(response.css('header h1::text').get())
		job["industry"] = self.clean_text(response.css('header h1::text').get())
		job["country"] = "Kenya"
		self.get_header_details(response.css('header .details li *::text').getall(), job)
		self.get_tagged_details(response.css('header .tags li span::text').getall(), job)

		divs = response.css('.content *::text').getall()
		titles = response.xpath('//h3/text() | //strong /text() | //bold/text()').getall()
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

		re_list = [
			{
				"re": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
				"fields": ["contact"]
			}
		]

		deadline_search = search(r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})", text, IGNORECASE)
		if deadline_search:
			job["deadline"] = deadline_search.group(0)
			job["year"] = "N/A"

		self.get_search_words(titles, re_list)

		self.regex_search(text, re_list, job)










		

