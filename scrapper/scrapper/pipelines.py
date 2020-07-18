# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
import os
from scrapy.exceptions import DropItem


class CsvWriterPipeline:
    def open_spider(self, spider):
        outputFiles = 1
        for entry in os.listdir():
            if entry.find('.csv') != -1:
                outputFiles+=1

        self.file = open(f"KEN Webscraping Job Posts-v{outputFiles}.csv", 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item:
            adapter = ItemAdapter(item)
            columns = adapter.field_names()
            writer = csv.DictWriter(self.file, fieldnames=columns)

            if self.file.tell() == 0:
                writer.writeheader()
            writer.writerow(adapter.asdict())


class InvalidEntryPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        values = adapter.asdict()
        empty = lambda field : not field
        empty_fields = filter(empty, list(values.values()))

        if len(list(empty_fields)) > 10:
            print("\n\n***************")
            print("Dropped")
            print("******************\n\n")
            raise DropItem("Too many empty values found.")

        return item