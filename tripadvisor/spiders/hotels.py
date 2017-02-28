import scrapy
from tripadvisor.items import HotelItem, RestaurantItem

class HotelSpider(scrapy.Spider):
    name = 'hotel'
    start_urls = ['https://www.tripadvisor.fr/Hotels-g11038886-Hauts_de_France-Hotels.html']

    def parse_review(self, response):
        item = HotelItem()
        item['date'] = response.xpath("//span[contains(@class,'ratingDate')]/@content").extract_first()
        item['content'] = response.xpath("//div[@class='entry']/p/text()").extract_first().replace("\n", "")
        item['rating'] = response.xpath("////span[@class='rate sprite-rating_s rating_s']/img/@alt").extract_first()[0]
        return(item)
        
        
    def parse_hotel(self, response):
        for href in response.xpath("//div[@class='quote']/a/@href"):
            url = response.urljoin(href.extract())
            yield(scrapy.Request(url, callback=self.parse_review))
            
        next_page = response.xpath("//a[@class='nav next rndBtn ui_button primary taLnk']/@href").extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield(scrapy.Request(url, self.parse_hotel))
    
            
    def parse(self, response):
        # Get the list of all hotels
        for href in response.xpath("//a[@class='property_title ']/@href"):
            url = response.urljoin(href.extract())
            yield(scrapy.Request(url, callback=self.parse_hotel))
            
        next_page = response.xpath("//a[@class='nav next ui_button primary taLnk']/@href").extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield(scrapy.Request(url, self.parse))
            
            
class RestaurantSpider(scrapy.Spider):
    name = 'restaurants'
    start_urls = ['https://www.tripadvisor.fr/Restaurants-g11038886-Hauts_de_France.html']

    def parse_review(self, response):
        item = RestaurantItem()
        item['date'] = response.xpath("//span[contains(@class,'ratingDate')]/@content").extract_first()
        item['content'] = response.xpath("//div[@class='entry']/p/text()").extract_first().replace("\n", "")
        item['rating'] = response.xpath("//span[@class='rate sprite-rating_s rating_s']/img/@alt").extract_first()[0]
        return(item)
        
    
    def parse(self, response):
        for href in response.xpath("//div[@class='geo_name']/a/@href"):
            url = response.urljoin(href.extract())
            yield(scrapy.Request(url, callback=self.parse_city))
            
        next_page = response.xpath("//a[@class='nav next rndBtn ui_button primary taLnk']/@href").extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield(scrapy.Request(url, self.parse))
            
            
    def parse_city(self, response):
        for href in response.xpath("//a[@class='property_title']/@href"):
            url = response.urljoin(href.extract())
            yield(scrapy.Request(url, callback=self.parse_restaurant))
            
        next_page = response.xpath("//a[@class='nav next rndBtn ui_button primary taLnk']/@href").extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield(scrapy.Request(url, self.parse_city))
            
    
    def parse_restaurant(self, response):
        for href in response.xpath("//div[@class='quote']/a/@href"):
            url = response.urljoin(href.extract())
            yield(scrapy.Request(url, callback=self.parse_review))
            
        next_page = response.xpath("//a[@class='nav next rndBtn ui_button primary taLnk']/@href").extract_first()
        if next_page:
            url = response.urljoin(next_page)
            yield(scrapy.Request(url, self.parse_restaurant))
            