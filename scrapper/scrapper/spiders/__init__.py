from logging import info
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
                yield sc.Request(url=metadata["url"], callback=self.parse_sites, cb_kwargs=dict(site=site, meta=metadata))

    def parse_sites(self, response, site, meta):
        for href in response.css(meta["link_selector"]).getall():
            is_full = search("^https|http.?", href)
            if not is_full:
                yield sc.Request(str(meta["domain"] + href), self.parse, cb_kwargs=dict(site=site))
            yield sc.Request(href, self.parse, cb_kwargs=dict(site=site))

    def parse(self, response, site):
        job = site.parse(response)
        yield job

    def get_sites(self):
        return [
            sites.brightermonday.BrighterMonday(),
            sites.jiji.Jiji()
        ]

				







