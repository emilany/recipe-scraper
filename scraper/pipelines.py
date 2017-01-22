# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
from scrapy.exceptions import DropItem


class ScraperPipelineExportJson(object):
    def __init__(self):
        self.file = codecs.open('allrecipes.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=False) + "," +"\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.close()

# class AllrecipesIngredientPipeline(object):
#     def process_item(self, item, spider):
#         for word in self.words_to_filter:
#             ingred = item['ingredients']
#             if word in ingred.lower():
#                 raise DropItem("Contains forbidden word: %s" % word)
#         else:
#             return item
