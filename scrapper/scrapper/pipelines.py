# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.loader import ItemLoader
import csv
import os
from scrapy.exceptions import DropItem


class CsvWriterPipeline:
    def open_spider(self, spider):
        outputFiles = 1
        for entry in os.listdir():
            if entry.find('.csv') != -1:
                outputFiles+=1
        
        self.items = list()
        self.file = open(f"KEN Webscraping Job Posts-v{outputFiles}.csv", 'w', newline='')

    def close_spider(self, spider):
        if self.items is not []:
            for item in self.items:
                adapter = ItemAdapter(item)
                columns = adapter.field_names()
                writer = csv.DictWriter(self.file, fieldnames=columns, restval='', extrasaction='ignore', delimiter=',', quoting=csv.QUOTE_NONNUMERIC, quotechar="\"")

                if self.file.tell() == 0:
                    writer.writeheader()
                writer.writerow(adapter.asdict())

        self.file.close()

    def process_item(self, item, spider):
        if item in self.items:
            self.items[self.items.index(item)]['readvertised'] = 'Y'
        else:
            item['ID'] = len(self.items) + 1
            self.items.append(item)


class InvalidEntryPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        values = adapter.asdict()
        empty = lambda field : not field
        empty_fields = filter(empty, list(values.values()))

        if len(list(empty_fields)) > 12 or values.get("country") != "Kenya":
            print("\n\n***************")
            print("Dropped")
            print("******************\n\n")
            raise DropItem("Too many empty values found.")

        return item
