import datetime
import os
import csv

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider

class Holiday(BaseSpider):
	name = "india_destinations"
	start_urls = ['https://www.holidayiq.com/holiday-packages/']
	
	def __init__(self):
		self.filename = "indiadestions%s.csv" %(str(datetime.datetime.now().date()))
		self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["destination", "url", "image"]
		self.csv_file.writerow(self.fields)
		
	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
			os.system('rm%s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file
	
	def parse(self, response):
		sel = Selector(response)
		#nodes = sel.xpath('//li[@class="col-xs-12 col-sm-8 col-md-8 col-lg-8"]')
		#for node in nodes:
		nodes = sel.xpath('//div[@class="pkg-top-images-section"]/ul[@class="grid cs-style-3"]/li/a')
		for node in nodes:
			url_text = ''.join(node.xpath('./@data-text').extract())
			url = ''.join(node.xpath('./@href').extract())
			image_url = ''.join(node.xpath('./figure/img/@src').extract())
			#title = ''.join(node.xpath('./figure/span[@class="pkg-grid-txt"]/text()').extract())
			csv_values = [url_text, url, image_url]
			self.csv_file.writerow(csv_values)
		
		