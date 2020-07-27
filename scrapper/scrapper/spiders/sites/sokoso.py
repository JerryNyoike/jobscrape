from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class Sokoso(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Sokoso",
			"base_url": "https://www.sokoso.co.ke/jobs/search?",
			"domain": 'https://https://www.sokoso.co.ke',
			"method": "GET",
			"search_param": "search",
            "next_page_selector": "ul.pagination li.page-item:last-child a.page-link::attr(href)",
			"link_selector": 'a.list-group-item-heading::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["name"]
		job["url"] = response.url
		job["jobTitle"] = response.css('h1.h2::text').get()
		job["company"] = response.xpath("//h1[@class='h2']/following-sibling::h4/text()")
		job["positions"] = 1
		job["readvertised"] = "N/A"
		job["country"] = "Kenya"

		titles = response.xpath('//h1 /text() | //h4 /text() | //strong /text() | //b/text()').getall()
		divs = response.css('div.container *::text').getall()
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