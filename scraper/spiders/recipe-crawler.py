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
    name = "allrecipes"
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
        item['url'] = response.css('link#canonicalUrl::attr(href)').extract_first()
        item['title'] = response.css('.recipe-summary__h1::text').extract_first()
        item['description'] = response.css('#metaDescription::attr(content)').extract_first()
        item['image'] = response.css('head > meta:nth-child(15)::attr(content)').extract_first()
        item['ingredients'] = response.css('.recipe-ingred_txt::text').extract()
        item['directions'] = response.css('.recipe-directions__list--item::text').extract()
        return item

class EatingWell(scrapy.Spider):
    name = "eatingwell"
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
        item['url'] = response.css('meta:nth-child(15)::attr(content)').extract_first()
        item['title'] = response.css('.recipeDetailSummaryDetails h3::text').extract_first()
        item['description'] = response.css('.recipeSubmitter p::attr(title)').extract_first()
        item['image'] = response.css('.recipeDetailSummaryImageContainer img::attr(src)').extract_first()
        item['ingredients'] = response.css('.listIngredients li span::text').extract()
        item['directions'] = response.css('.recipeDirectionsList li span::text').extract()
        return item

class Chowhound(scrapy.Spider):
    name = "chowhound"
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
        item['url'] = response.css('meta:nth-child(18)::attr(content)').extract_first()
        item['title'] = response.css('.fr_r_info h1::text').extract_first()
        item['description'] = response.css('meta::attr(content)').extract_first()
        item['image'] = response.css('meta:nth-child(33)::attr(content)').extract_first()
        item['ingredients'] = response.css('.freyja_box81 li::text').extract()
        item['directions'] = response.css('.freyja_box82 li::text').extract()
        return item

class SimplyRecipes(scrapy.Spider):
    name = "simplyrecipes"
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
        item['url'] = response.css('head > link::attr(href)').extract_first()
        item['title'] = response.css('.entry-header h1::text').extract_first()
        item['description'] = response.css('meta:nth-child(20)::attr(content)').extract_first()
        item['image'] = response.css('meta:nth-child(4)::attr(content)').extract_first()
        item['ingredients'] = response.css('.ingredient::text').extract()
        item['directions'] = response.css('.instructions p::text').extract()
        return item

class Epicurious(scrapy.Spider):
    name = "epicurious"
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
        item['url'] = response.css('.main meta:nth-child(2)::attr(content)').extract_first()
        item['title'] = response.css('.title-source h1::text').extract_first()
        item['description'] = response.css('.dek p::text').extract_first()

        image = response.css('.photo-wrap img::attr(srcset)').extract_first()
        item['image'] = "http:" + image
        
        item['ingredients'] = response.css('.ingredients li::text').extract()
        item['directions'] = map(unicode.strip, response.css('.preparation-steps li::text').extract())
        return item

