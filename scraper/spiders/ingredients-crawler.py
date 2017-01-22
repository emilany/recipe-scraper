import scrapy

from scrapy.http import Request
from scraper.items import *

#url list
URLAllrecipes = "http://allrecipes.com/recipes/84/healthy-recipes/?page=%d"
URLEatingwell = "http://www.eatingwell.com/recipes/?page=%d"
URLSimplyrecipes = "http://www.simplyrecipes.com/page/%d/?s=healthy"
URLEpicurious = "http://www.epicurious.com/search/?special-consideration=healthy&content=recipe&page=%d"
URLChowhound = "http://www.chowhound.com/recipes/healthy?page=%d"

class Allrecipes(scrapy.Spider):
    name = "allrecipes-ingr"
    download_timeout = 10000
    allowed_domains = ["allrecipes.com"]
    start_urls = ["http://allrecipes.com/recipes/84/healthy-recipes/"]

    def __init__(self):
        self.page_number = 1

    def parse(self, response):
        for recipe in response.css('.grid-col--fixed-tiles'):
            datakey = recipe.css('.favorite::attr(data-id)').extract_first()
            url = "http://allrecipes.com/recipe/{}".format(datakey)
            yield Request(url, callback=self.parserecipe)

            # follow pagination links
            self.page_number += 1
            yield Request(URLAllrecipes % self.page_number)

    # getting actual recipe content from site
    def parserecipe(self, response):
        item = RecipeItems()
        item['ingredients'] = response.css('.recipe-ingred_txt::text').extract()
        return item

class EatingWell(scrapy.Spider):
    name = "eatingwell-ingr"
    download_timeout = 10000
    allowed_domains = ["eatingwell.com"]
    start_urls = [URLEatingwell % 1]

    def __init__(self):
        self.page_number = 1

    def parse(self, response):
        for recipe in response.css('.gridCol--fixed-tiles'):
            datakey = recipe.css('.favorite::attr(data-id)').extract_first()
            url = "http://eatingwell.com/recipe/{}".format(datakey)
            yield Request(url, callback=self.parserecipe)

            # follow pagination links
            self.page_number += 1
            yield Request(URLEatingwell % self.page_number)

    # getting actual recipe content from site
    def parserecipe(self, response):
        item = RecipeItems()
        item['ingredients'] = response.css('.listIngredients li span::text').extract()
        return item

class Chowhound(scrapy.Spider):
    name = "chowhound-ingr"
    download_timeout = 10000
    allowed_domains = ["chowhound.com"]
    start_urls = [URLChowhound % 1]

    def __init__(self):
        self.page_number = 1

    def parse(self, response):
        for recipe in response.css('.fr_box_rechub'):
            url = recipe.css('a::attr(href)').extract_first()
            yield Request(url, callback=self.parserecipe)

            # follow pagination links
            self.page_number += 1
            yield Request(URLChowhound % self.page_number)

    # getting actual recipe content from site
    def parserecipe(self, response):
        item = RecipeItems()
        item['ingredients'] = response.css('.freyja_box81 li::text').extract()
        return item

class SimplyRecipes(scrapy.Spider):
    name = "simplyrecipes-ingr"
    download_timeout = 10000
    allowed_domains = ["simplyrecipes.com"]
    start_urls = [URLSimplyrecipes % 1]

    def __init__(self):
        self.page_number = 1

    def parse(self, response):
        for recipe in response.css('.entry-list li'):
            url = recipe.css('a::attr(href)').extract_first()
            yield Request(url, callback=self.parserecipe)

            # follow pagination links
            self.page_number += 1
            yield Request(URLSimplyrecipes % self.page_number)

    # getting actual recipe content from site
    def parserecipe(self, response):
        item = RecipeItems()
        item['ingredients'] = response.css('.ingredient::text').extract()
        return item

class Epicurious(scrapy.Spider):
    name = "epicurious-ingr"
    download_timeout = 10000
    allowed_domains = ["epicurious.com"]
    start_urls = ["http://www.epicurious.com/search/?special-consideration=healthy&content=recipe"]

    def __init__(self):
        self.page_number = 1

    def parse(self, response):
        for recipe in response.css('.recipe-result-item'):
            item = RecipeItems()
            recipeurl = recipe.css('.summary h4 a::attr(href)').extract_first()
            url = "http://www.epicurious.com{}".format(recipeurl)
            yield Request(url, callback=self.parserecipe)

            # follow pagination links
            self.page_number += 1
            yield Request(URLEpicurious % self.page_number)

    # getting actual recipe content from site
    def parserecipe(self, response):
        item = RecipeItems()
        item['ingredients'] = response.css('.ingredients li::text').extract()
        return item

