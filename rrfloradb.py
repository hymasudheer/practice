import datetime
import os
import csv
import mysql.connector

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
#from scrapy import signals
#from scrapy.xlib.pydispatch import dispatcher

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class Rrflora(BaseSpider):

	name = "floradb"
	start_urls = ['https://rrflora.com/']
	
	def __init__(self, *args, **kwargs):
		""" Connecting to database"""
		self.conn = mysql.connector.connect(host="localhost", user="root", password='hyma22$', db="practice", charset='utf8', use_unicode=True)
		self.cur = self.conn.cursor()

	def parse(self, response):
		sel = Selector(response)
		#title_node = sel.xpath('//h2[@class="entry-title"]')
		nodes = sel.xpath('//div[@id="posts"]/article')
		for node in nodes:
			title = ''.join(node.xpath('.//h2[@class="entry-title"]/a/text()').extract())
			desc = ''.join(node.xpath('.//div[@class="entry-content"]/p/text()').extract())
			link = ''.join(node.xpath('.//h2[@class="entry-title"]/a/@href').extract())
			img = ''.join(node.xpath('.//div[@class="entry-media"]/@style').extract())
			#import pdb;pdb.set_trace()
			yield Request(link, callback=self.parse_next, meta={'title_main':title, 'desc':desc, 'image':img})
			
	def parse_next(self, response):
		sel = Selector(response)
		title = response.meta['title_main']
		desc = response.meta['desc']
		image = response.meta['image']
		images= sel.xpath('//div[@class="entry-content"]/figure')
		for pics in images:
			pic = ''.join(pics.xpath('./a/@href').extract())
			#import pdb;pdb.set_trace()
			qry = 'insert into rrflora(title, image_desc, image_1, image_2) values(%s, %s, %s, %s)'
			values = (title, desc, image, pic)
			self.cur.execute(qry, values)
			#import pdb;pdb.set_trace()
			self.conn.commit()