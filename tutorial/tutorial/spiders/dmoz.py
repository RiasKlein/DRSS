import scrapy

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["http://library.si.edu/donate/major-supporters"]
    start_urls = [
        "http://library.si.edu/donate/major-supporters"
        ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.txt'
        text = str(response.body)
        logic = True
        i = 0
        while(logic):
            ind1 = text.find('<')
            ind2 = text.find('>',ind1)
            ind3 = text.find("<!--")
            ind4 = text.find("-->",ind3)
            
            
            if(ind3 <= ind1):
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
                    
            i+=1
            if ind1 == -1 or ind2 == -1:
                logic = False

        with open(filename, 'wb') as f:
            f.write(text)
