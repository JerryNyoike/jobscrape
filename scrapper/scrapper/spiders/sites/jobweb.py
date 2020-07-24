from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class JobWeb(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "JobWeb",
			"base_url": "https://jobwebkenya.com/?",
			"domain": 'https://jobwebkenya.com',
			"method": "GET",
			"search_param": "s",
            "next_page_selector": "div.paging a.next::attr(href)",
			"link_selector": 'div#titlo strong a::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["name"]
		job["url"] = response.url
		job["jobTitle"] = response.css('h1.title::text').get()
		job["positionLevel"] = "N/A"
		job["positions"] = 1
		job["uploadDate"] = response.css('div.date strong::text').get()
		job["year"] = response.css('div.date strong::text').get().strip().split(" ")[-1]
		job["readvertised"] = "N/A"
		job["country"] = "Kenya"

		titles = response.xpath('//strong /text() | //b/text()').getall()
		divs = response.css('div.section_content *::text').getall()
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