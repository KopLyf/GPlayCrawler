# -*- coding: utf-8 -*-
import re
import json
import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.linkextractors import LinkExtractor
from scrapy.http import FormRequest
from app.items import GoogleItem


class GoogleSpider(CrawlSpider):
    name = "google"
    allowed_domains = ["play.google.com"]
    start_urls = [
        'http://play.google.com/',
        'https://play.google.com/store/apps/details?id=com.instagram.android'
    ]
    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details",)), callback='parse_app', follow=True),
    ]

    def __init__(self, *a, **kw):
        super(GoogleSpider, self).__init__(*a, **kw)

    def parse_app(self, response):

    	item = GoogleItem()
    	item['url'] = response.url
        item['appid'] = response.url.split("?id=")[-1].split("&")[0]
        item['score'] = response.xpath("//div[@class='score']").xpath("text()").extract()
        item['datePublished'] = response.xpath("//div[@itemprop='datePublished']").xpath("text()").extract()
        item['fileSize'] = response.xpath("//div[@itemprop='fileSize']").xpath("text()").extract()
    	item['numDownloads'] = response.xpath("//div[@itemprop='numDownloads']").xpath("text()").extract()
        item['softwareVersion'] = response.xpath("//div[@itemprop='softwareVersion']").xpath("text()").extract()
        item['operatingSystems'] = response.xpath("//div[@itemprop='operatingSystems']").xpath("text()").extract()
        item['contentRating'] = response.xpath("//div[@itemprop='contentRating']").xpath("text()").extract()
        item['thumbs'] = response.xpath("//div[@class='thumbnails']/img").xpath("@src").extract()
        item['icon'] = response.xpath("//div[@class='cover-container']/img[@class='cover-image']").xpath("@src").extract()
        item['description'] = response.xpath("//div[@itemprop='description']/div").xpath("text()").extract()
        item['permissions'] = []
        item['reviews'] = []
        item['continued'] = True

        doc_url = "https://play.google.com/store/xhr/getdoc"
        doc_form = {"ids": item['appid'], "xhr": '1'}
        yield FormRequest(doc_url, callback=self.parse_doc, formdata=doc_form, meta={'item': item})


    def parse_doc(self, response):
        item = response.meta['item']
        data = re.findall("\{.*\}", response.body, re.S)
        pat = re.findall(",,\[\[.*", data[0], re.S)
        if len(pat) > 0:
            pers = re.findall("\[\".*\",\d\]", pat[0])
            for per in pers:
                text = json.loads(per)[0].encode('utf-8')
                if text not in item['permissions']:
                    item['permissions'].append(text)

        pageNum = 0
        url = "https://play.google.com/store/getreviews"
        formdata = {"id":item['appid'], "reviewType":'0', "reviewSortOrder":'4', "pageNum":str(pageNum), "xhr":'1'}
        request = FormRequest(url, callback=self.parse_review, formdata=formdata, meta={'item':item, 'pageNum':0, 'url':url})
        yield request

    def parse_review(self, response):
        response_data = re.findall("\[\[.*", response.body)
        item = response.meta['item']
        if response_data:
            text = json.loads(response_data[0] + ']')
            sell = scrapy.Selector(text=text[0][2])
            blocks = sell.xpath('//div[@class="single-review"]')
            reviews = []
            for block in blocks:
                author = block.xpath('div[@class="review-header"]/div[@class="review-info"]/span[@class="author-name"]/text()').extract()
                date = block.xpath('div[@class="review-header"]/div[@class="review-info"]/span[@class="review-date"]/text()').extract()
                star = block.xpath('div[@class="review-header"]/div[@class="review-info"]/div[@class="review-info-star-rating"]/div').xpath("@aria-label").extract()
                title = block.xpath('div[@class="review-body with-review-wrapper"]/span[@class="review-title"]/text()').extract()
                body = block.xpath('div[@class="review-body with-review-wrapper"]/text()').extract()
                year = date[0][-4:]
                if year != '2016' and year != '2017' and year != '2015':
                    item['continued'] = False
                    break
                else:
                    reviews.append({
                        'author': author[0].strip().encode('utf-8'),
                        'date': date[0].encode('utf-8'),
                        'star': star[0].encode('utf-8'),
                        'title': '' if len(title) == 0 else title[0].encode('utf-8'),
                        'body': ''.join(x for x in body).strip().encode('utf-8')
                    })
            item['reviews'].extend(reviews)

        pageNum = response.meta['pageNum'] + 1
        url = response.meta['url']
        if item['continued'] and pageNum < 3:
            formdata = {"id":item['appid'], "reviewType":'0', "reviewSortOrder":'4', "pageNum":str(pageNum), "xhr":'1'}
            yield FormRequest(url, callback=self.parse_review, formdata=formdata, meta={'item':item, 'pageNum':pageNum, 'url':url})
        else:
            for key, value in item.items():
                if key == 'reviews':
                    continue
                if type(value) == list:
                    item[key] = [x.encode('utf-8') for x in value]
                if type(value) == str:
                    item[key] = value.encode('utf-8')
            yield item
