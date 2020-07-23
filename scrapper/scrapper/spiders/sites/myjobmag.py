from logging import info
from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class MyJobMag(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "My Job Mag",
			"base_url": "https://www.myjobmag.co.ke/search/jobs?",
			"domain": 'https://www.myjobmag.co.ke',
			"method": "GET",
			"search_param": "q",
			"link_selector": 'li.mag-b h2 a::attr(href)'
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["name"]
		job["url"] = response.url
		job["jobTitle"] = response.css('a.subjob-title::text').get()
		job["jobType"] = response.xpath("//ul[@class='job-key-info']/li[span[@class='jkey-title']/text() = 'Job Type']/span[@class='jkey-info']/a/text()").get()
		job["positionLevel"] = "N/A"
		job["positions"] = 1
		job["uploadDate"] = response.css('div#posted-date::text').get()
		job["year"] = response.css('div#posted-date::text').get().split(",")[-1]
		job["deadline"] = response.css('div.read-date-sec-li:nth-child(2)::text').get()
		job["town"] = response.xpath("//ul[@class='job-key-info']/li[span[@class='jkey-title']/text() = 'Location']/span[@class='jkey-info']/a/text()").get()
		job["readvertised"] = "N/A"
		job["company"] = response.css('li.job-industry a::text').get()
		job["technology"] = response.xpath("//ul[@class='job-key-info']/li[span[@class='jkey-title']/text() = 'Job Field']/span[@class='jkey-info']/a/text()").get()
		job["employmentType"] = response.xpath("//ul[@class='job-key-info']/li[span[@class='jkey-title']/text() = 'Job Type']/span[@class='jkey-info']/a/text()").get()
		job["industry"] = response.css('li.job-industry a::text').get()
		job["country"] = "Kenya"

		titles = response.xpath('//strong /text() | //bold/text()').getall()
		divs = response.css('#job-description-holder *::text').getall()
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