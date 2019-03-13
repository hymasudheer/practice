from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider 

import datetime
import os
import csv

des = ['romantic', 'historical', 'religious', 'beaches', 'city', 'hill+stations', 'adventure', 'wildlife']

class Happytravel(BaseSpider):
	name = "travel"
	start_urls = ['https://timesofindia.indiatimes.com/travel/destinations']
	
	def __init__(self):
		self.filename = "dest%s.csv" % (str(datetime.datetime.now().date()))
		self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["title", "tags"]
		self.csv_file.writerow(self.fields)
		
	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
			os.system('rm%s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file

	def parse(self, response):
		sel = Selector(response)
		#index = sel.xpath('//div[@class="pagination2"]//a[@class="next"]/@lastindex').extract()
		node = sel.xpath('//div[@class="clearfix tab_data"]//li/a')
		for x in node:
			destination_link = ''.join(x.xpath('./@href').extract())
			yield Request(destination_link, callback = self.parse_next)
			
	def parse_next(self, response):
		sel = Selector(response)
		page_no = sel.xpath('//div[@class="pagination2"]//a[contains(@class, "number-btn index")]/text()').extract()
		for d in des:
			url = 'https://timesofindia.indiatimes.com/travel/travel_destination.cms?curpg=1&ajax=1&query=mData_GuideGenre:%22'+d+'%22'
			for p in page_no:
				complete_url = 'https://timesofindia.indiatimes.com/travel/travel_destination.cms?curpg='+str(p)+'&ajax=1&query=mData_GuideGenre:%22'+d+'%22'
				yield Request(complete_url, callback=self.parse_last)
				
	def parse_last(self, response):
		sel = Selector(response)
		nodes = sel.xpath('//div[@id="content_wrapper"]//div[contains(@class, "box1 one-third")]')
		for node in nodes:
			title = (''.join(node.xpath('.//h3/a/text()').extract()).replace('\n', '')).encode("utf-8")
			tags = ','.join(node.xpath('.//p[@class="toggle tags"]//a/text()').extract())
			csv_values = [title, tags]
			self.csv_file.writerow(csv_values)
			#import pdb;pdb.set_trace()