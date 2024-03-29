from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class NewJobs(site.Site):
	
	def __init__(self):
		self.meta = {
			"name": "New Jobs",
			"base_url": "https://newjobskenya.com/?",
			"domain": 'https://newjobskenya.com',
			"method": "GET",
			"search_param": "query",
			"get_args": {"category": " "},
			"link_selector": '.wpjb-column-title a::attr(href)',
			"next_page_selector": "#wpjb-paginate-links a.next::attr(href)"
		}
		super().__init__(self.meta)


	def parse(self, response):
		job = Job()
		job["ID"] = 1
		job["website"]= self.meta["name"]
		job["url"] = response.url
		job["jobTitle"] = response.xpath('//h1[@class="entry-title"]/text()').get()
		job["jobType"] = response.xpath('//span[@itemprop="employmentType"]/text()').get()
		job["positionLevel"] = response.xpath('//h1[@class="entry-title"]/text()').get()
		job["positions"] = 1
		job["uploadDate"] = response.xpath('//span[@class="updated"]/text()').get()
		job["year"] = response.xpath('//span[@class="updated"]/text()').get().split(',')[-1].strip()
		job["deadline"] = "N/A"
		job["town"] = response.xpath('//span[@itemprop="address"]/text()').get()
		job["reavertised"] = "N/A"
		job["company"] = response.css('.wpjb-job-company::text').get()
		job["technology"] = response.xpath('//span[@itemprop="occupationalCategory"]/text()').get()
		job["employmentType"] = response.xpath('//span[@itemprop="employmentType"]/text()').get()
		job["industry"] = response.xpath('//span[@itemprop="occupationalCategory"]/text()').get()
		job["country"] = "Kenya"
		
		titles = response.xpath('//h3/text() | //strong /text() | //b/text()').getall()
		divs = response.css('.wpjb-job-content *::text').getall()
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










		


