# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class GoogleItem(scrapy.Item):
    url = scrapy.Field()
    appid = scrapy.Field()
    score = scrapy.Field()
    datePublished = scrapy.Field()
    fileSize = scrapy.Field()
    numDownloads = scrapy.Field()
    softwareVersion = scrapy.Field()
    operatingSystems = scrapy.Field()
    contentRating = scrapy.Field()
    thumbs = scrapy.Field()
    icon = scrapy.Field()
    description = scrapy.Field()
    reviews = scrapy.Field()
    permissions = scrapy.Field()
    continued = scrapy.Field()
