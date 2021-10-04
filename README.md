# Job Scrape
This projects purpose is to obtain data on job postings from multiple sources and aggregate it into one comma separated value (CSV) file.

## Technologies used
1. [Python programming language](https://www.python.org/)
2. [Scrapy](https://scrapy.org/). This Python package enables us to extract the job data from websites by using regular expressions and xpath expressions

## Project Structure
- The folder *./scraper/scraper/spiders/sites/* contains the web crawlers defined as Python classes. These web crawlers define rules for extracting job posting information from the websites using either xpath or regular expressions.
- The file *./scraper/scraper/spider/\__init\__.py* contains an implementation for the class **JobSpider** where all the web crawlers are instantiated and run in order to extract the information. Th JobSpider class also defines the keywords to search for in the respective web sites.
- The file *./scraper/scraper/items.py* contains an abstraction of a job item defining the most important attributes that the web crawlers will look for in the websites.
- The file *./scraper/scraper/pipelines.py* contains processing rules for the data that is exracted and returned by the web crawlers. The Class **CSVWriterPipeline** defines rules for how the CSV file will be created while the class **InvalidEntryPipeline** defines rules for when to exclude a job item from the CSV file.

## Directions for Running
1. Install the dependencies in a [virtualenvironment]().
2. Run the command `scrapy crawl jobspider` within the virtual environment.

## Sample output
The CSV file is given as output and is stored within the *./scraper/scraper/* directory.

## Contributors
[Braxton Muimi](https://github.com/Brackie)

[Jerry Nyoike](https://github.com/JerryNyoike)
