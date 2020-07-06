from urllib.parse import urlencode

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
        ]

def createUrls(baseUrl, identifier, searchWords=keywords):
    ''' This function creates the search urls to be crawled by the spiders.
    baseUrl : the root of the website
    identifier : the name of the query parameter used by the site while performing a search
    searchWords : the words to search on the website
    '''
    createQueryPairs = lambda keyword : {identifier: keyword}
    makeUrl = lambda keywordPair : baseUrl+urlencode(keywordPair)

    keywordPairs = list(map(createQueryPairs, searchWords))

    return list(map(makeUrl, keywordPairs))
