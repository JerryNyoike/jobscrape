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
			"get_args": {"category": ""},
			"link_selector": '.wpjb-column-title a::attr(href)'
		}
		self.search_words = [
			{
				"fields": ["description"],
				"titles": "Description, Summary, Details, Opportunity, The Role, Overview"
			},
			{
				"fields": ["requirements", "skills"],
				"titles": "Qualifications, Candidate Profile, Nice To Have, Competencies, Skills, Experience, Requirements"
			},
			{
				"fields": ["responsibilities"],
				"titles": "Responsibilities, Role Purpose, Tasks, Duties"
			},
			{
				"fields": ["salary"],
				"titles": "Salary"
			}
		]
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
		titles = response.xpath('//h3/text() | //strong /text() | //bold/text()').getall()
		divs = response.css('.wpjb-job-content *::text').getall()
		return job	

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

		self.get_search_words(titles, re_list)

		self.regex_search(text, re_list, job)










		


