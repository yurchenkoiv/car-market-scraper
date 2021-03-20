# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Car(scrapy.Item):
    price = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    trans = scrapy.Field()
    fuel = scrapy.Field()
    km = scrapy.Field()
    kw = scrapy.Field()
    date = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
