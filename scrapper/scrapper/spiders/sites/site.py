class Site(object):

	"""A Base class to define class variables for different site subclasses"""

	spider = None

	def __init__(self, meta):
		self.meta = meta

	def clean_soup(soup):
		soup = soup.replace('\n','')
		soup = soup.replace('\t','')
		return soup
