import itertools
import scrapy
from Msrp.items import CarDataItem, CarDataItemLoader


class MsrpSpider(scrapy.Spider):
    name = 'TestSpider'
    allowed_domains = ['https://www.jdpower.com']

    def start_requests(self):
        makes = ["Acura", "Aston-Martin"]

        def makes_urls(value):
            urls = []
            urls.append([f'https://www.jdpower.com/Cars/2019/{make}' for make in value])
            urls.append([f'https://www.jdpower.com/Cars/2018/{make}' for make in value])

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
