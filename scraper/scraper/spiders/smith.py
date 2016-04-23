import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

class DmozSpider(scrapy.Spider):
    name = "smith"
    allowed_domains = ["library.si.edu"]
    start_urls = [
        "https://library.si.edu/donate/make-a-donation"
        #,"http://library.si.edu/donate/major-supporters"
        ]
    download_delay = 2
    
    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            logic = False
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            if 'Supporters' in str(title):
                string = str(link)
                string = string.strip('[')
                string = string.strip(']')
                string = string[1:len(string)]
                string = string.strip('\'')
                
                print "http://library.si.edu" + string
                return scrapy.Request(url=("http://library.si.edu" + string),
                        callback=self.parse_donors)
    
    def parse_donors(self, response):
        self.logger.info("Visited %s", response.url)
        for sel in response.xpath('//td/div'):
            title = sel.xpath('text()').extract()
            print title
        
