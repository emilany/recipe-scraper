# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join

class RecipeItems(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    image = scrapy.Field()
    ingredients = scrapy.Field()
    directions = scrapy.Field()
