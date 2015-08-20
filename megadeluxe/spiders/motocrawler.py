# -*- coding: utf-8 -*-
# Copyright (c) 2015 Datacratic Inc.  All rights reserved.
# @Author:             alexis
# @Email:              atremblay@datacratic.com
# @Date:               2015-08-19 18:22:25
# @Last Modified by:   alexis
# @Last Modified time: 2015-08-20 07:59:05
# @File Name:          motocrawler.py

from scrapy.spiders import CrawlSpider, Rule
# from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from urllib import urlencode
from urlparse import urlparse, urlunparse, parse_qs
from megadeluxe.items import MegadeluxeMotoImage


class MotoSpider(CrawlSpider):
    """MotoSpider"""

    name = "megadeluxe"
    allowed_domains = ["megadeluxe.com"]
    start_urls = ["http://megadeluxe.com/category/motorcycles"]
    rules = (
        # Rule(
        #     LxmlLinkExtractor(
        #         restrict_xpaths=['//a[@class="next"]']
        #         ),
        #     callback="printURL",
        #     follow=True
        # ),
        Rule(
            LxmlLinkExtractor(
                allow=["megadeluxe.com/motorcycles/.*"]
                ),
            callback='parse_article',
            follow=True
        ),
    )

    def parse_article(self, response):
        for url in response.xpath('//div[contains(@class, "post")]//img/@src').extract():

            u = urlparse(url)
            query = parse_qs(u.query)
            query.pop('resize', None)
            query.pop('fit', None)
            u = u._replace(query=urlencode(query, True))
            return MegadeluxeMotoImage(url=urlunparse(u))


    def printURL(self, response):
        print("GOOOOTTTTT {}".format(response.url))