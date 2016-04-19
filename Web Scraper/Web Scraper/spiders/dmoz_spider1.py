import scrapy

from tutorial.items import DmozItem

class DmozSpider(scrapy.Spider):
    name = "dmoz1"
    allowed_domains = ["library.si.edu"]
    start_urls = [
        "http://library.si.edu/donate/major-supporters"
        ]

    def parse(self, response):
        for sel in response.xpath('//td/div'):
            title = sel.xpath('text()').extract()
            print title
