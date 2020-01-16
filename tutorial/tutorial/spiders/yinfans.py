import scrapy
from scrapy import Request
from urllib import parse

class yinfans(scrapy.Spider):
    name="yinfans"
    allowed_domains=['yinfans.me']
    start_urls=['http://www.yinfans.me/']

    def parse(self,response):
        node_list=response.xpath('//*[@id="post_container"]//div[@class="thumbnail"]')
        for node in node_list:
            url=node.xpath('a/@href').extract_first("")
            img=node.xpath('a/img/@src').extract_first("")
            yield Request(url=parse.urljoin(response.url,url),meta={"front_image_url":img},callback=self.parse_detail)


        next_page_url=response.xpath('//div[@class="pagination"]/a[@class="next"]/@href').extract_first("")
        yield Request(url=parse.urljoin(response.url,next_page_url),callback=self.parse)

    def parse_detail(self,response):
        # title=response.xpath('//*[@id="content"]//h1').extract_first("")
        name=response.xpath('//*[@id="post_content"]/p[2]/text()[1]').extract_first("").replace("\n", "")
        douban=response.xpath('//*[@id="post_content"]/p[2]/text()[10]').extract_first("").replace("\n", "")
        with open('result.md','a+') as f:
            f.write('{}|{}\n'.format(name,douban))


