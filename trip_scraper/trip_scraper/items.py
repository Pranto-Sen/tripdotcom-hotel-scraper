import scrapy

class HotelItem(scrapy.Item):
    Title = scrapy.Field()
    Rating = scrapy.Field()
    Country = scrapy.Field()
    Location = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
    Price = scrapy.Field()
    Hotel_img = scrapy.Field()
