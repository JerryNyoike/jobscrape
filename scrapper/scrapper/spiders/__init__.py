# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import scrapy as sc
from . import sites
import logging


class JobSpider(sc.Spider)
    name = "jobs"
    jobs = list()
    sites = get_sites()
    sites.Site.set_spider(self)

    def get_sites(self):
    	return [
    		sites.brightermonday.BrighterMonday(),
    		sites.jiji.Jiji()
    	]

    def start_requests(self):
        for site in sites:
        	for metadata in site.meta:
            	yield sc.Request(url=metadata.url, callback=self.parse_sites)

	def parse_sites(self, response):
		meta = get_current_site(response.url)
		for href in response.css(meta.link_selector).getall():
			is_full = search("^[https]|[http]", href)
			if not is_full:
				yield scrapy.Request(str(meta.domain + href), self.parse)
            yield scrapy.Request(href, self.parse)

    def parse(self, response):
		site = get_current_site(response.url)
		job = site.parse(response)
		jobs.add(job)
		logging.info(job)

    def get_current_site(page):
    	for site in self.sites:
	    	for metadata in site.meta:
	    		if metadata.url == page:
	    			return metadata

				







