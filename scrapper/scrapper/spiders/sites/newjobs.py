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
		job["website"]= self.meta["domain"]
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

		contact_search = search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text, IGNORECASE)
		if contact_search:
			job["contact"] = contact_search.group(0)	

		deadline_search = search(r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})", text, IGNORECASE)
		if deadline_search:
			job["deadline"] = deadline_search.group(0)

		re_list = self.get_search_words(titles)

		self.regex_search(text, re_list, job)










		


