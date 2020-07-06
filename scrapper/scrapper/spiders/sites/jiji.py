from . import site
from scrapper.items import Job
from re import search, IGNORECASE


class Jiji(site.Site):
	"""Site class for https://www.ajiradigital.go.ke/home"""

	def __init__(self):
		self.meta = [
			{
				"name": "Jiji.ke",
				"url": "https://jiji.co.ke/computing-and-it-jobs",
				"domain": 'https://jiji.co.ke/',
				"method": "GET",
				"link_selector": 'a.b-list-advert__item-image::attr(href)'
			}
		]
		super().__init__(self.meta)

	def parse(self, response):
		job = Job()
		job["ID"]= 1
		job["website"] = self.meta[0]["domain"]
		job["url"] = response.url
		title = self.clean_text(response.css('.b-advert-title-inner::text').get())
		job["jobTitle"] = title
		job["positions"] = 1
		job["description"] = title
		job["technology"] = title
		job["uploadDate"] = self.clean_text(response.css('time::text').get())
		job["town"] = self.clean_text(response.css('.b-advert-info-statistics::text').get())
		job["year"] = "2020"
		job["contact"] = "N/A"
		job["readvertised"] = "N/A"
		job["country"] = "Kenya"
		divs = response.css(".b-advert-attributes *::text").getall()
		self.get_details(divs, job)
		return job

	def get_details(self, divs, job):
		divs = self.clean_page(divs)
		text = self.clean_text(" ".join(divs))

		company = search(r".?Name(.*?)Job?", text, IGNORECASE)
		if company:
			job["company"] = company.group(1)
			job["industry"] = company.group(1)
			text = text.replace(company.group(1), '')

		jobType = search(r".?Type(.*?)Carrer?", text, IGNORECASE)
		if jobType:
			job["jobType"] = jobType.group(1)
			job["employmentType"] = jobType.group(1)
			text = text.replace(jobType.group(1), '')

		positionLevel = search(r".?Level(.*?)Application?", text, IGNORECASE)
		if positionLevel:
			job["positionLevel"] = positionLevel.group(1)
			text = text.replace(positionLevel.group(1), '')

		deadline = search(r".?Deadline(.*?)Responsibilities?", text, IGNORECASE)
		if deadline:
			job["deadline"] = deadline.group(1)
			text = text.replace(deadline.group(1), '')

		responsibilities = search(r".?Responsibilities(.*?)Requirements?", text, IGNORECASE)
		if responsibilities:
			job["responsibilities"] = responsibilities.group(1)
			text = text.replace(responsibilities.group(1), '')

		requirements = search(r".?Skills(.*?)Minimum?", text, IGNORECASE)
		if requirements:
			job["requirements"] = requirements.group(1)
			job["skills"] = requirements.group(1)
			text = text.replace(requirements.group(1), '')

		qualifications = search(r".?Requirements(.*?)Minimum?", text, IGNORECASE)
		if responsibilities:
			job["requirements"] = str(job["requirements"] + qualifications.group(1))
			text = text.replace(qualifications.group(1), '')

		salary = search(r".?Salary(.*?)$", text, IGNORECASE)
		if salary:
			job["salary"] = salary.group(1)