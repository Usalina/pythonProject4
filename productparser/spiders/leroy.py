import scrapy
from scrapy.http import HtmlResponse
from productparser.items import ProductparserItem
from scrapy.loader import ItemLoader


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru/search/?q=ковер&family=kovry-201709&suggest=true']

    def parse(self, response):
        next_page = response.xpath("////a[@data-qa-pagination-item='right']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@data-qa='product-name']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.good_parse)

    def good_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=ProductparserItem(), response=response)
        loader.add_xpath('name', "//h1[@itemprop='name']/text()")
        loader.add_xpath('image', "//source[contains(@media, 'only screen and (min-width: 1024px)')]/@srcset")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('url', response.url)
        yield loader.load_item()

        # name = response.xpath("//h1[@itemprop='name']/text()").get()
        # image = response.xpath("//source[contains(@media, 'only screen and (min-width: 1024px)')]/@srcset").getall()
        # url = response.url
        # price = response.xpath("//meta[@itemprop='price']/@content").get()
        # yield ProductparserItem(name=name, image=image, url=url, price=price)

