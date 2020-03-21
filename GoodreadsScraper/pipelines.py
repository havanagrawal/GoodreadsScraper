# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from scrapy import signals


class JsonLineItemSegregator(object):
    @classmethod
    def from_crawler(cls, crawler):
        output_file_suffix = crawler.settings.get("OUTPUT_FILE_SUFFIX", default="")
        return cls(crawler, output_file_suffix)

    def __init__(self, crawler, output_file_suffix):
        self.types = {"book", "author"}
        self.output_file_suffix = output_file_suffix
        self.files = set()
        crawler.signals.connect(self.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(self.spider_closed, signal=signals.spider_closed)

    def spider_opened(self, spider):
        self.files = {name: open(name + "_" + self.output_file_suffix + '.jl', 'a+b') for name in self.types}
        self.exporters = {name: JsonLinesItemExporter(self.files[name]) for name in self.types}

        for e in self.exporters.values():
            e.start_exporting()

    def spider_closed(self, spider):
        for e in self.exporters.values():
            e.finish_exporting()

        for f in self.files.values():
            f.close()

    def process_item(self, item, spider):
        item_type = type(item).__name__.replace("Item", "").lower()
        if item_type in self.types:
            self.exporters[item_type].export_item(item)
        return item
