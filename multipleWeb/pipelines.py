# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MultiplewebPipeline(object):
    def process_item(self, item, spider):
        with open("data_total.txt", "a") as f:
            f.write(str(item['body']))



