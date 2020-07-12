from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class Template(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Site name",
			"url": "https://www.greatkenyanjobs.com/index.php/jobseeker/component/job/jobsearchresults",
			"domain": 'site domain',
			"method": "POST",
			"": {},
			"link_selector": 'selector for follow link'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta[0]["domain"]
		job["url"] = response.url
		job["jobTitle"] = response.css('selector::text').get()
		job["jobType"] = response.css('selector::text').get()
		job["positionLevel"] = response.css('selector::text').get()
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
		return job	

	def get_description(self, divs, job):
		divs = self.clean_page(divs)
		text = self.clean_text(' '.join(divs))

		re_list = [
			{
				"re": r".?KeyWord(.*?)KeyWord?",
				"fields": [""]
			}
		]

		self.regex_search(text, re_list, job)










		


