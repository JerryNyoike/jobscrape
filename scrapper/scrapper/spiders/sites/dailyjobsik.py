from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class DailyJobsIK(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Daily Jobs In Kenya",
			"base_url": "https://www.dailyjobsinkenya.com/?",
			"domain": 'https://www.dailyjobsinkenya.com',
			"method": "GET",
			"search_param": "s",
			"link_selector": 'article.post h2 a::attr(href)',
			"next_page_selector": '.pagination a.next::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["name"]
		job["url"] = response.url
		job["jobTitle"] = response.css('article.post h2 a::text').get()
		job["jobType"] = "N/A"
		job["positions"] = 1
		job["uploadDate"] = response.css('div#meta_authorl::text').get()
		job["readvertised"] = "N/A"
		job["company"] = response.css('article.post h2 a::text').get().split(" at ")[-1]
		job["employmentType"] = "N/A"
		job["country"] = "Kenya"

		titles = response.xpath('//h3/text() | //strong /text() | //b/text()').getall()
		divs = response.css('article.post *::text').getall()
		self.get_description(titles, divs, job)
		return job	


	def get_description(self, titles, divs, job):
		divs = self.clean_page(divs)
		titles = self.clean_page(titles)
		text = self.clean_text(' '.join(divs))

		self.get_contacts(text, job)
		self.get_deadline(text, job)

		re_list = self.get_search_words(titles)

		self.regex_search(text, re_list, job)
