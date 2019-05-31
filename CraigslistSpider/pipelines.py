# -*- coding: utf-8 -*-
import sqlite3 as lite
import scrapy
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from scrapy.contrib.pipeline.images import ImagesPipeline

class DatabasePipeline(object):
    def process_item(self, item, spider):
        return item



class TestPipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super(TestPipeline, self).__init__(store_uri, settings=settings, download_func=download_func)

        self.con = lite.connect('boards.db')
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS resultsTable (ID INTEGER PRIMARY KEY, \
                                                ImageURL TEXT, \
                                                Message TEXT, \
                                                ImgHash TEXT    UNIQUE, \
                                                postURL TEXT    UNIQUE, \
                                                Title   TEXT    UNIQUE  );")

    def process_item(self, item, spider):

        super(TestPipeline, self).process_item(item, spider)
        
        self.cur.execute("INSERT OR IGNORE INTO resultsTable (ImageURL, Message, ImgHash, postURL, Title) \
            VALUES(?, ?, ?, ?, ?)", (item['image_urls'][0], item['message'][0], item['imgHash'][0], item['postURL'][0], item['Title'][0]))

        print(item['postURL'][0])
        
        self.con.commit()
        return item

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    #def open_spider(self, spider):
        #self.con = lite.connect('dog.db')
        #self.cur = self.con.cursor()

    def close_spider(self, spider):
        self.con.close()


