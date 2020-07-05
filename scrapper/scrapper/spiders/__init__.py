# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import logging
from . import sites
import scrapy as sc
from re import search
from scrapper.items import Job
from scrapy.loader import ItemLoader


class JobSpider(sc.Spider):
    name = "jobs"

    def start_requests(self):
        self.sites = self.get_sites()
        for site in self.sites:
            for metadata in site.meta:
                yield sc.Request(url=metadata["url"], callback=self.parse_sites)

    def parse_sites(self, response):
        _, meta = self.get_current_site(response.url)
        for href in response.css(meta["link_selector"]).getall():
            is_full = search("^[https]|[http]", href)
            if not is_full:
                yield sc.Request(str(meta["domain"] + href), self.parse)
            yield sc.Request(href, self.parse)

    def parse(self, response):
        site, _ = self.get_current_site(response.url)
        job = site.parse(response)
        logging.info(job)
        yield job

    def get_current_site(self, page):
        for site in self.sites:
            for metadata in site.meta:
                logging.info(metadata["url"] + " VS " + page)
                if metadata["url"] == page:
                    return site, metadata

    def get_sites(self):
        return [
            sites.brightermonday.BrighterMonday(),
            sites.jiji.Jiji()
        ]

				







