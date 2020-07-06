from logging import info
from re import search, IGNORECASE


class Site(object):

	"""A Base class to define class variables for different site subclasses"""

	def __init__(self, meta):
		self.meta = meta
	
	def clean_text(self, text):
		if text:
			text = text.replace('\n','')
			text = text.replace('\t','')
			double_space = search(r".*?(\s*).?", text)
			if double_space:
				text = text.replace(double_space.group(1), '')
		return text

	def clean_page(self, output):
		divs = list()
		if output:
			for i, text_node in enumerate(output):	
				html_present = search(r".*?(<.*?>).?", text_node)
				if html_present:
					output[i] = text_node.replace(html_present.group(1), '')

				double_space = search(r".*?(\s*).?", text_node)
				if double_space:
					output[i] = text_node.replace(double_space.group(1), '')

				trailing_space = search(r"^(\s*).?|.?(\s*)$", text_node)
				if trailing_space:
					output[i] = text_node.replace(trailing_space.group(1), '')
		return output

