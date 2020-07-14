from logging import info
from re import search, sub, IGNORECASE
from urllib.parse import urlencode

class Site(object):

	'''A Base class to define class variables for different site subclasses'''

	def __init__(self, meta):
		self.meta = meta
	
	def createUrls(self, baseUrl, identifier, searchWords, params={}):
		''' This function creates the search urls to be crawled by the spiders.
		baseUrl : the root of the website
		identifier : the name of the query parameter used by the site while performing a search
		searchWords : the words to search on the website
		returns the urls for the searches in a list which can then be used by start_urls or start_requests in a spider
		'''
		createQueryPairs = lambda keyword : {identifier: keyword}

		makeUrl = lambda keywordPair : baseUrl+urlencode(keywordPair)

		params = list(map(createQueryPairs, searchWords))

		return list(map(makeUrl, params))

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
				for field in regex["fields"]:
					job[field] = search_result.group(1)
				text = text.replace(search_result.group(1), '')
	
	def clean_text(self, text):
		'''This function replaces new-line characters, trailing spaces and replaces 
		multiple spaces with one space
		text: the text to replace
		'''
		if text:
			text = text.replace('\n', '')
			text = sub(r".*?(<.*?>)", '', text)
			text = sub(r"^[\s]*|[\s]*$", '', text)
			text = sub(r"[\s\r*]{2,}", ' ', text)
		return text

	def clean_page(self, output):
		'''This function takes a list of strings and calls the clean_text function on them
		output: list of strings
		'''
		divs = list()
		if output:
			for i, text_node in enumerate(output):	
				output[i] = self.clean_text(text_node)
		return output
	
