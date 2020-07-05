# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os


class CsvWriterPipeline:
    def open_spider(self, spider):
        outputFiles = 1
        for entry in os.listdir():
            if entry.find('.csv') is not -1:
                outputFiles+=1

        self.file = open(f"KEN Webscraping Job Posts-v{outputFiles}.csv", 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        columns = adapter.field_names()
        writer = csv.DictWriter(self.file, fieldnames=fields)

        writer.writeheader()
        writer.writerow(adapter.asdict())
