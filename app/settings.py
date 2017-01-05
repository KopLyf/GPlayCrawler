# -*- coding: utf-8 -*-

# Scrapy settings for app project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'app'

SPIDER_MODULES = ['app.spiders']
NEWSPIDER_MODULE = 'app.spiders'
DOWNLOAD_DELAY = 1
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'app (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
  'app.pipelines.MongoDBPipeline': 100
}

MONGODB_SERVER = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DB = 'GoogleApp'
MONGODB_COLLECTION = 'app'
