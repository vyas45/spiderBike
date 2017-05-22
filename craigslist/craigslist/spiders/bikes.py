# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from firebase import db_init

#Sanitize the arguments
#attrname is a list of attributes which is usually of the form: 
# Name, condition, engine displacement(cc), fuel , color, title status, transmission
#[u'2004 honda shadow aero', u'excellent', u'gas', u'black', u'clean', u'manual']
def bikeInfo(bikeAttrs):
    print "Attributes are ", bikeAttrs



class BikesSpider(scrapy.Spider):
    name = 'bikes'
    allowed_domains = ['craigslist.org']
    start_urls = ['https://sfbay.craigslist.org/search/mcy/']


    def parse(self, response):
        #get individual bike elements from the page
        bikes = response.xpath('//p[@class="result-info"]')
        #Extract the titles from every bike element
        for bike in bikes:
            title = bike.xpath('a/text()').extract_first()
            #Get the address of the bike, address == location
            #The last part gets the '()' out of '(south san jose)'
            address = bike.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first("")[2:-1]
            price = bike.xpath('span[@class="result-meta"]/span[@class="result-price"]/text()').extract_first("")
            relative_url = bike.xpath('a/@href').extract_first()
            absolute_url = response.urljoin(relative_url)
            yield Request(absolute_url, callback=self.parse_page,meta={'URL':absolute_url, 'Title':title, 'Address':address, 'Price':price})

        #Get the next set up pages till all pages are crawled
        relative_next_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_url = response.urljoin(relative_next_url)

        #Keep yielding till all the pages are done and keep calling self 
        #yield Request(absolute_next_url, callback=self.parse)

    #This method goes over every bike individually to scrape specific data
    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        price = response.meta.get('Price')

        #Using join as the descrition can be more than one line long
        desc = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())

        #Get the bike attributes
        bikeAttrs = response.xpath("//p[@class='attrgroup']/span/b/text()").extract()


        bikeInfo(bikeAttrs)

        #Get the locaiton of the bike and store it as a list of lat and long
        maplocation = response.xpath("//div[contains(@id,'map')]")
        lat = ''.join(maplocation.xpath('@data-latitude').extract())
        longi = ''.join(maplocation.xpath('@data-longitude').extract())

        #Firebase setup
        db, user = db_init()

        #Data being pused in
        #Currently the key is the bike title (TODO: Think of Sanitizing the name)
        #Things that can be added to the DB:
        #Price, Location, Condition, Color, Description,
        db_data = {'Url': url, 'Price':price, 'Location' : {'Lat':lat, 'Long':longi}, 'Desciption':desc}
        #db.child("agents").child("Bikes").push(db_data, user['idToken'])

        #Check if the key exists, if it does update else insert a new record
        db.child("agents").child(bikeAttrs[0]).update(db_data, user['idToken'])

        #yield{'URL': url, 'Title': title, 'Address':address, 'Price':price} 
