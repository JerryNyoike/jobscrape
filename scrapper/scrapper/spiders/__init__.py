from logging import info
from . import sites
import scrapy as sc
from re import search
from scrapper.items import Job
from scrapy.loader import ItemLoader

keywords = [
    "Software Engineer",
    "Tech Support Engineer",
    "DevOps Engineer",
    "Test Engineer",
    "Network Security Engineer",
    "Network Engineer",
    "Computer Hardware",
    "Program Engineer",
    "Computer Scientist",
    "Digital Business Manager",
    "IT Specialist",
    "Systems Analyst",
    "Business Systems Analyst",
    "Programmer",
    "Coder",
    "Network Architect",
    "Information Security Analyst",
    "Programmer Analyst",
    "Systems Security Advisor",
    "Business Intelligence Analyst",
    "Application Developer",
    "Systems Developer",
    "Assistant Systems Developer",
    "Backend Developer",
    "Frontend Developer",
    "Software Developer",
    "Mobile Applications Developer",
    "Program Developer",
    "Web Developer",
    "Product Developer",
    "Game Developer",
    "Chief Technical Officer",
    "Chief Information Officer",
    "Software Project Manager",
    "Head of e-commerce",
    "Director of Digital",
    "Director of e-commerce",
    "Data Analyst",
    "Data Engineer",
    "Data Scientist",
    "Data Expert",
    "SEO Analyst",
    "Data Miner",
    "Database Administrator",
    "Marketing Strategist",
    "Graphic Designer",
    "UX Designer",
    "Digital Experience Manager",
    "Digital Copywriter",
    "New Media Manager",
    "New Media Officer",
    "Webmaster",
    "UX Researcher",
    "Video Creator",
    "Creative Strategist",
    "Creative Associate",
    "Communications Associate",
    "Social Media Associate",
    "Social Media Influencer",
    "Social Media Specialist",
    "Content Strategist",
    "Social Media guru",
    "Evangelist",
    "Social Media Manager",
    "Community Manager",
    "Social Media Officer",
    "Content Manager",
    "Chief Digital Marketing",
    "Senior Art Director",
    "Chief Creative",
    "Chief Strategist",
    "Digital Marketing Executive",
]

class JobSpider(sc.Spider):
    name = "jobs"

    def start_requests(self):
        '''This function iterates over a list of site objects to find links to job pages'''
        self.sites = self.get_sites()
        for site in self.sites:
            get_args = {}
            if 'get_args' in site.meta:
                get_args = site.meta['get_args']

            start_urls = site.createUrls(site.meta["base_url"], site.meta["search_param"], keywords, get_args)
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
            sites.coopstaffing.CoopStaffing(),
            sites.jik.Jik(),
            sites.r4kenya.R4kenya(),
            sites.careerjet.CareerJet(),
            sites.careerpoint.CareerPoint(),
            sites.newjobs.NewJobs(),
            sites.dailyjobsik.DailyJobsIK(),
            sites.emploi.Emploi()
        ]
