# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient

class ProductparserPipeline:
    def process_item(self, item, spider):
        print()
        return item

class LeroyImgPiplines(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['image']:
            for img in item['image']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['image'] = [itm[1] for itm in results if itm[0]]
        return item


class ProductparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client['leroy']

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection._insert_one(item)
        return item