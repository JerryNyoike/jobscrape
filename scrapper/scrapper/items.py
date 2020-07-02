import scrapy


class Job(scrapy.Item):
    ID: scrapy.Field()
    website: scrapy.Field()
    url: scrapy.Field()
    jobTitle: scrapy.Field()
    jobType: scrapy.Field()
    positionLevel: scrapy.Field()
    positions: scrapy.Field()
    uploadDate: scrapy.Field()
    year: scrapy.Field()
    deadline: scrapy.Field()
    town: scrapy.Field()
    contact: scrapy.Field()
    readvertised: scrapy.Field()
    salary: scrapy.Field()
    company: scrapy.Field()
    technology: scrapy.Field()
    description: scrapy.Field()
    employmentType: scrapy.Field()
    skills: scrapy.Field()
    industry: scrapy.Field()
    responsibilities: scrapy.Field()
    requirements: scrapy.Field()
    country: scrapy.Field()
