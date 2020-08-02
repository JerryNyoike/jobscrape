from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE
from urllib.parse import urlencode, quote


class StarClassifieds(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Star Classifieds",
			"base_url": "https://www.the-star.co.ke/classifieds/jobs/",
			"domain": 'https://www.the-star.co.ke/',
			"method": "GET",
			"search_param": "q",
			"get_args": {"usp": "true"},
            "next_page_selector": "div#paginate a.paginate-next::attr(href)",
			"link_selector": 'section.product a.product-link::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["name"]
		job["url"] = response.url
		job["positionLevel"] = "N/A"
		job["positions"] = 1
		job["readvertised"] = "N/A"
		job["country"] = "Kenya"

		titles = response.xpath('//h1 /text() | //h2 /text() | //h3 /text() | //h4 /text() | //strong /text() | //b/text()').getall()
		divs = response.css('body *::text').getall()
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


	def createUrls(self, baseUrl, identifier, searchWords, params):
		''' This function creates the search urls to be crawled by the spiders.
		baseUrl : the root of the website
		identifier : the name of the query parameter used by the site while performing a search
		searchWords : the words to search on the website
		returns the urls for the searches in a list which can then be used by start_urls or start_requests in a spider
		'''
		makeUrl = lambda keyword : baseUrl + '-'.join(keyword.lower().split(" ")) + '.html?' + urlencode(params, quote_via=quote)
		return list(map(makeUrl, searchWords))