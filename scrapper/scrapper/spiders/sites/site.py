from re import search


class Site(object):

	"""A Base class to define class variables for different site subclasses"""

	spider = None

	def __init__(self, meta):
		self.meta = meta

	@classmethod
	def set_spider(spider):
		self.spider = spider