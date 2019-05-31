# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DatabaseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CustomSpider(scrapy.Item):
	image_urls = scrapy.Field()
	images = scrapy.Field()
	message = scrapy.Field()
	imgHash = scrapy.Field()
	image_paths = scrapy.Field()
	postURL = scrapy.Field()
	Title = scrapy.Field()

class testSpider(scrapy.Item):
	pageTitle = scrapy.Field()
