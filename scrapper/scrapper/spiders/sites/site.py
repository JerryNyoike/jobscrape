from logging import info
from re import search, findall, sub, escape, IGNORECASE
from urllib.parse import urlencode, quote


class Site(object):

	'''A Base class to define class variables for different site subclasses'''

	def __init__(self, meta):
		self.meta = meta
		self.search_words = [
			{
				"fields": ["company"],
				"titles": "Company Name, Industry"
			},
			{
				"fields": ["jobType", "employmentType"],
				"titles": "Job Type, Employment Type"
			},
			{
				"fields": ["description"],
				"titles": "Description, Summary, Opportunity, Program Description, Details, Role, Overview"
			},
			{
				"fields": ["requirements"],
				"titles": "Requirements, Candidate Profile, Competencies, Languages, Experience, Education"
			},
			{
				"fields": ["skills"],
				"titles": "Qualifications, Personal Attributes, Desired Skills, Desirable Qualities, Nice, Competencies, Experience"
			},
			{
				"fields": ["responsibilities"],
				"titles": "Responsibilities, Specific Tasks, Expected, Duties"
			},
			{
				"fields": ["salary"],
				"titles": "Salary, Remuneration, Salary Scale, Compensation"
			},
			{
				"fields": ["positionLevel", "technology", "industry"],
				"titles": "Position Level, Rank, Job Category, Industry, Technology"
			},
			{
				"fields": ["town"],
				"titles": "Location, Situated, Town, City, Place, State"
			},
			{
				"fields": ["deadline"],
				"titles": "Deadline, Submitted By, Not later than, No later than, Later than, Valid Until"
			}
		]

	
	def createUrls(self, baseUrl, identifier, searchWords, params):
		''' This function creates the search urls to be crawled by the spiders.
		baseUrl : the root of the website
		identifier : the name of the query parameter used by the site while performing a search
		searchWords : the words to search on the website
		returns the urls for the searches in a list which can then be used by start_urls or start_requests in a spider
		'''
		createQueryPairs = lambda keyword : {identifier: keyword}

		makeUrl = lambda keywordPair : baseUrl+urlencode(keywordPair, quote_via=quote)

		params = list(map(createQueryPairs, searchWords))

		return list(map(makeUrl, params))


	def get_search_words(self, titles):
		'''This function creates a list of regex strings to search for job content
		depending on the key words available that match key job attributes
		titles: a list of key words
		re_list: a list of regex strings and the job fields to be filled
		'''
		re_list = list()
		titles = self.drop_empty_fields(titles)
		for search_word in self.search_words:
			for i, title in enumerate(titles):
				for word in title.split(' '):
					word = sub(r"[^a-zA-Z0-9]", '', word)
					if (len(word) >= 4) and (search(fr'{escape(word)}', search_word["titles"], IGNORECASE)):
						next_title = ""
						if (i + 1) < len(titles):
							next_title = titles[i+1]
						re = fr'{escape(title)}(.+?){escape(next_title)}'
						re_list.append({
							"re": re,
							"fields": search_word["fields"]
						})
		return re_list


	def regex_search(self, text, re_list, job):
		'''This function does a regex search in a string of text for a 
		list of regex strings provided and sets the result to a field in a job item
		text: the text to search
		re_list: a list of regex strings and the job fields to be filled
		job: the job to be populated
		'''
		for regex in re_list:	
			search_result = search(regex["re"], text, IGNORECASE)
			if search_result:
				self.populate_fields(regex["fields"], search_result.group(1), job)
				text = text.replace(search_result.group(1), '')


	def get_contacts(self, text, job):
		'''This function does a regex search for emails and adds the matches to contact field'''
		contacts = findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|(?:[0-9\-]{8,15})", text)
		if contacts:
			for contact in contacts:
				self.populate_fields(["contact"], contact, job)


	def get_deadline(self, text, job):
		'''This function does a regex search for dates and adds the matches to deadline, uploadDate field'''
		dates = findall(r"(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})", text)
		if dates:
			for date in dates:
				self.populate_fields(["uploadDate", "deadline"], date, job)


	def populate_fields(self, fields, text, job):
		'''This functions takes a list of job fields that share data and puts text in all of them'''
		for field in fields:
			if (field in job) and job[field]:
				job[field] = str(job[field] + ", " + text)
			else:
				job[field] = text


	def clean_text(self, text):
		'''This function replaces new-line characters, trailing spaces and replaces 
		multiple spaces with one space
		text: the text to replace
		'''
		if text:
			text = text.strip()
			text = text.replace('\n', '')
			text = sub(r"^[^a-zA-Z0-9]+$", '', text)
			text = sub(r"[!#$%^&*()\":{}|<>]+?", '', text)
			text = sub(r".*?(<.*?>)", '', text)
			text = sub(r":\xa0", '', text)
			text = sub(r"[\s]{2,}", ' ', text)
		return text


	def clean_page(self, output):
		'''This function takes a list of strings and calls the clean_text function on them
		output: list of strings
		'''
		output = self.drop_empty_fields(output)
		clean = lambda text : self.clean_text(text)
		return list(map(clean, output))


	def drop_empty_fields(self, divs):
		'''This function takes a list of Strings and removes the empt ones from the list
		divs: list of strings
		'''
		not_empty = lambda div : not (not self.clean_text(div))
		return list(filter(not_empty, divs))


	def next_page_url(self, url):
		return url.replace(url[-1], str(int(url[-1])+1))
