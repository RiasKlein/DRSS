import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request

class DmozSpider(scrapy.Spider):
    name = "scrapeWebsite"
    allowed_domains = ["library.si.edu"]
    start_urls = [
        "https://library.si.edu/"
        ]
    download_delay = 2

        #finds weblink matching key
    def parse(self, response):
        for sel in response.xpath('//ul/li'):
            logic = False
            title = sel.xpath('a/text()').extract()
            link = sel.xpath('a/@href').extract()
            #key is Supporters
            if 'Supporters' in str(title):
                string = str(link)
                string = string.strip('[')
                string = string.strip(']')
                string = string[1:len(string)]
                string = string.strip('\'')
                
                #print "http://library.si.edu" + string
                return scrapy.Request(url=("http://library.si.edu" + string),
                            callback=self.parse_donors)

    def parse_donors(self, response):
        filename = response.url.split("/")[-2] + '.txt'
        text = str(response.body)
        
        while(True):
            ind1 = text.find('<')
            ind2 = text.find('>',ind1)
            ind3 = text.find("<!--")
            ind4 = text.find("-->",ind3)
            if ind1 == -1 and ind3 == -1:
                break
            
            if(ind3 <= ind1 and ind3 != -1):
                ind1 = ind3
                ind2 = ind4
                print(str(ind1) + " " + str(ind2) + "\n" + text[ind1:ind2+3])
                
                if(ind1 != 0 and ind2 != len(text)):
                    #print text[0:ind1] + text[ind2+3:len(text)]
                    text = text[0:ind1] + text[ind2+3:len(text)]
                elif(ind1 == 0):
                    text = text[ind2+3:len(text)]
                elif(ind2 == len(text)):
                    text = text[0:ind1]
                    
            else:
                print(str(ind1) + " " + str(ind2) + "\n" + text[ind1:ind2+1])
                
                if(ind1 != 0 and ind2 != len(text)):
                    text = text[0:ind1] + text[ind2+1:len(text)]
                elif(ind1 == 0):
                    text = text[ind2+1:len(text)]
                elif(ind2 == len(text)):
                    text = text[0:ind1]
                    

            with open(filename, 'wb') as f:
                f.write(text)

