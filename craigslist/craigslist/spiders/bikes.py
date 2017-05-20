# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from firebase import db_init

#Sanitize the arguments
def sanitizeArgs(title, address, price, absolute_url):
    print "Title is ", title


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

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('Title')
        address = response.meta.get('Address')
        price = response.meta.get('Price')

        #Using join as the descrition can be more than one line long
        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())
        attname = response.xpath('//*[@id="postingbody"]/text()').extract()
        

        sanitizeArgs(title, address, price, absolute_url)
        db, user = db_init()
        #db_data = {'URL': url, 'Title': title, 'Address':address, 'Price':price, 'Description':description}
        #db.child("agents").child("Bikes").push(db_data, user['idToken'])

        #yield{'URL': url, 'Title': title, 'Address':address, 'Price':price} 
