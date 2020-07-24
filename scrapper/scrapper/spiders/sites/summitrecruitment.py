from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class SummitRecruitment(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "Summitrecruitment Search",
			"base_url": "https://www.summitrecruitment-search.com/jobs/job-category/",
			"domain": 'https://www.summitrecruitment-search.com',
			"method": "GET",
            "search_param": "none",
			"link_selector": 'h2.entry-title a::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["name"]
		job["url"] = response.url
		job["jobTitle"] = response.css('h1.entry-title::text').get().split("–")[0]
		job["jobType"] = response.xpath("//div[@class='single-job-meta']/ul/li[span[@class='job-meta-title']/text() = 'Job Type:']/span[@class='job-meta-content']/text()").get()
		job["positionLevel"] = response.xpath("//div[@class='single-job-meta']/ul/li[span[@class='job-meta-title']/text() = 'Career Level:']/span[@class='job-meta-content']/text()").get()
		job["positions"] = 1
		job["uploadDate"] = "N/A"
		job["year"] = response.xpath("//div[@class='single-job-meta']/ul/li[span[@class='job-meta-title']/text() = 'Deadline:']/span[@class='job-meta-content']/text()").get().strip().split(" ")[-1]
		job["deadline"] = response.xpath("//div[@class='single-job-meta']/ul/li[span[@class='job-meta-title']/text() = 'Deadline:']/span[@class='job-meta-content']/text()").get()
		job["town"] = response.xpath("//div[@class='single-job-meta']/ul/li[span[@class='job-meta-title']/text() = 'Location:']/span[@class='job-meta-content']/text()").get()
		job["readvertised"] = "N/A"
		job["company"] = "N/A"
		job["technology"] = response.css('h1.entry-title::text').get().split("–")[0]
		job["employmentType"] = response.xpath("//div[@class='single-job-meta']/ul/li[span[@class='job-meta-title']/text() = 'Job Type:']/span[@class='job-meta-content']/text()").get()
		job["industry"] = response.css('h1.entry-title::text').get()
		job["country"] = "Kenya"

		titles = response.xpath('//strong /text() | //b/text()').getall()
		divs = response.css('div.entry-content *::text').getall()
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
		makeUrl = lambda keyword : baseUrl + '-'.join(keyword.lower().split(" ")) + '/'
		return list(map(makeUrl, searchWords))
