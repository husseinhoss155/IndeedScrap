import scrapy
pages=1
class Spider(scrapy.Spider):
    name = 'jobs'

    start_urls = ['https://eg.indeed.com/jobs?q=python%20developer&l&from=searchOnHP&vjk=9505375c8deee979']

    def parse(self, response):
        for job in response.css('ul.jobsearch-ResultsList>li'):
            title = job.css('h2>a>span::text').get()
            location = job.css('div.companyLocation::text').get()
            compname = job.css('span.companyName::text').get()
            if title ==None and location == None and compname == None:
                continue
            if compname == None:
                compname = job.css('span.companyName>a::text').get()
            yield {
                'title' : title,
                'company name':compname,
                'location' : location
            }

        for box in response.css('div.pagination>ul.pagination-list>li'):
            try:
                url = box.css('a').attrib['href']
            except:
                continue
        next_page = url
        if next_page != None:
            yield response.follow(url=next_page,callback=self.parse)