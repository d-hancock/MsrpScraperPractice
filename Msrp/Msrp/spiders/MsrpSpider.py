# -*- coding: utf-8 -*-
import scrapy
from typing import List
import itertools
import scrapy
from Msrp.items import CarDataItem, CarDataItemLoader


class MsrpSpider(scrapy.Spider):
    name = 'MsrpSpider'
    allowed_domains = ['']

    def start_requests(self):
        makes: List[str] = ['Acura', 'Aston-Martin', 'BMW', 'Buick', 'Cadillac',
                            'Chevrolet', 'Chrysler', 'Dodge', 'FIAT', 'Ford', 'GMC', 'Honda',
                            'Hummer', 'Hyundai', 'INFINITI', 'Jaguar', 'Jeep', 'Kia',
                            'Land-Rover', 'Lexus', 'Lincoln', 'Lotus', 'Mazda', 'Mercedes-Benz', 'Mitsubishi', 'Nissan',
                            'Oldsmobile', 'Panoz', 'Plymouth', 'Pontiac', 'Porsche',
                            'Ram-Truck', 'Scion', 'Subaru',
                            'Tesla-Motors', 'Toyota',
                            'Volkswagen', 'Volvo']

        def makes_urls(makes):
            urls = []
            urls.append([f"https://www.jdpower.com/Cars/2019/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2018/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2017/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2016/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2015/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2014/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2013/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2012/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2011/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2010/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2009/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2008/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2007/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2006/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2005/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2004/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2003/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2002/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2001/{make}" for make in makes])
            urls.append([f"https://www.jdpower.com/Cars/2000/{make}" for make in makes])

            urls = list(itertools.chain.from_iterable(urls))
            # urls = [y for x in urls for y in x]

            return urls

        urls = makes_urls(makes)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for vehicle in response.css('div.veh-spacer'):
            loader = CarDataItemLoader(item=CarDataItem(), response=response)
            loader.add_xpath('full_name', '//div[@class="veh-icons__title"]/text()').extract()
            loader.add_xpath('year', '//div[@class="veh-icons__title"]/text()').extract()
            loader.add_xpath('make', '//div[@class="veh-icons__title"]/text()').extract()
            model_loader = loader.nested_css('div.veh-spacer')
            model_loader.add_xpath('full_name', './div[2]/a/div/text()')
            model_loader.add_xpath('msrp_high',
                                   './div/div[2]/div[2]/div[1]/div/span[@class="veh-group__attribute-value"]/text()')
            model_loader.add_xpath('msrp_low',
                                   './div/div[2]/div[2]/div[1]/div/span[@class="veh-group__attribute-value"]/text()')
            yield loader.load_item()


