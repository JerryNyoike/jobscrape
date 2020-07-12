from logging import info
from . import sites
from . import config
import scrapy as sc
from re import search
from scrapper.items import Job
from scrapy.loader import ItemLoader


class JobSpider(sc.Spider):
    name = "jobs"

    def start_requests(self):
        '''This function iterates over a list of site objects to find links to job pages'''
        self.sites = self.get_sites()
        for site in self.sites:
            start_urls = config.createUrls(site.meta["base_url"], site.meta["search_param"])
            for url in start_urls:
                yield sc.Request(url=url, callback=self.parse_sites, cb_kwargs=dict(site=site, meta=site.meta))

    def parse_sites(self, response, site, meta):
        '''This functions iterates over a list of links to jobs on a site
        The response from the page is passed to the parse function for processing
        response: the response from a site giving a list of links to job pages
        site: object representing the site being scrapped
        meta: metadata on the site
        '''
        for href in response.css(meta["link_selector"]).getall():
            if not self.url_is_full(href):
                yield sc.Request(str(meta["domain"] + href), self.parse, cb_kwargs=dict(site=site))
            else:
                yield sc.Request(href, self.parse, cb_kwargs=dict(site=site))
        
        if 'next_page_selector' in meta:
            next_page = response.css(meta['next_page_selector']).get()
            if next_page:
                if self.url_is_full(next_page):
                    yield sc.Request(url=next_page, callback=self.parse_sites, cb_kwargs=dict(site=site, meta=meta))
                else:
                    yield sc.Request(str(meta["domain"] + next_page), self.parse_sites, cb_kwargs=dict(site=site, meta=meta))
    
    @classmethod
    def url_is_full(self, url):
        return search(r"^https.?|^http.?", url)

    def parse(self, response, site):
        '''This function passes the response from a job page to the parse 
        function in the respective site object
        response: response from the job page
        site: site object being scrapped
        '''
        job = site.parse(response)
        yield job

    def get_sites(self):
        '''This function returns a list of site objects representing sites to be scrapped'''
        return [
            sites.brightermonday.BrighterMonday(),
            sites.jiji.Jiji(),
            sites.bestjobs.BestJobs(),
            sites.coopstaffing.CoopStaffing()
            sites.jik.Jik(),
        ]
