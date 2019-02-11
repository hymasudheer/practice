import datetime
import os
import csv

from scrapy.spider import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class YoutubeSpider(BaseSpider):
	name = 'floranext'
	start_urls = ['https://rrflora.com/']
	
	def __init__(self):
		self.filename = "floranext%s.csv" % (str(datetime.datetime.now().date()))
		self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["title", "desc", "image"]
		self.csv_file.writerow(self.fields)
		
	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
			os.system('rm%s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file
	
	def parse(self, response):
		selector = Selector(response)
		article_nodes = selector.xpath('//div[@id="posts"]/article')
		next_page = ''.join(selector.xpath('//div[@class="nav-previous"]/a/@href').extract())
		if next_page is not None:
			for node in article_nodes:
				title = ''.join(node.xpath('./div[@class="entry-inner"]//header/h2/a/text()').extract())
				link = ''.join(node.xpath('./div[@class="entry-inner"]//header/h2/a/@href').extract())
				desc = ''.join(node.xpath('.//div[@class="entry-content"]/p/text()').extract())
				image = ''.join(node.xpath('./div[@class="entry-media"]/@style').extract())
				#import pdb;pdb.set_trace()
				
				yield Request(link, callback=self.parse_next, meta={'title_main': title, 'desc': desc, 'image': image, 'next_page':next_page})
		#else:
			#break
	def parse_next(self, response):
		sel = Selector(response)
		title = response.meta['title_main']
		desc  = response.meta['desc']
		image = response.meta['image']
		next_page = response.meta['next_page']
		image_nodes = sel.xpath('//div[@class="entry-content"]/figure')
		for image_node in image_nodes:
			pic = image_node.xpath('./a/@href').extract()
			csv_values = [title, desc, pic]
			self.csv_file.writerow(csv_values)
		yield Request(next_page, callback=self.parse)
		