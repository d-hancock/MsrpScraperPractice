# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join


class CarDataItemLoader(ItemLoader):

    def full_name_processor(self, value):
        x = value.replace(' models', '')
        return x.strip()

    def strip_processor(self, value):
        return value.strip()

    def year_processor(self, value):
        x = value.split()
        return x[0]

    def msrp_low_processor(self, value):
        x = value.replace('$', '')
        y = x.split()
        return float(y[0].replace(',', ''))

    def msrp_high_processor(self, value):
        x = value.replace('$', '')
        y = x.split()
        return float(y[-1].replace(',', ''))

    default_input_processor = TakeFirst()
    default_output_processor = TakeFirst()

    full_name_in = full_name_processor
    full_name_out = Join(separator=" ")

    year_in = year_processor

    make_in = strip_processor

    model_in = strip_processor

    msrp_high_in = msrp_high_processor

    msrp_low_in = msrp_low_processor


class CarDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    full_name = scrapy.Field()
    year = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    msrp_high = scrapy.Field()
    msrp_low = scrapy.Field()
