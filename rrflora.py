import datetime
import os
import csv

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
class Rrflora(BaseSpider):

	name = "flora"
	start_urls = ['https://rrflora.com/']

	def __init__(self):
		self.filename = "rrflora%s.csv" % (str(datetime.datetime.now().date()))
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
		sel = Selector(response)
		#title_node = sel.xpath('//h2[@class="entry-title"]')
		nodes = sel.xpath('//div[@id="posts"]/article')
		for node in nodes:
			title = ''.join(node.xpath('.//h2[@class="entry-title"]/a/text()').extract())
			desc = ''.join(node.xpath('.//div[@class="entry-content"]/p/text()').extract())
			link = ''.join(node.xpath('.//h2[@class="entry-title"]/a/@href').extract())
			img = ''.join(node.xpath('.//div[@class="entry-media"]/@style').extract())
			yield Request(link, callback=self.parse_next, meta={'title_main': title, 'desc': desc, 'image': image})
			
	def parse_next(self, response):
		sel = Selector(response)
		title = response.meta['title_main']
		desc = response.meta['desc']
		image = response.meta['image']
		next_page = ''.join(sel.xpath('//div[@class="nav-previous"]/a/@href').extract())
		images= sel.xpath('//div[@class="entry-content"]/figure')
		for pics in images:
			pic = pics.xpath('./a/@href').extract()
			csv_values = [title, desc, pic]
			self.csv_file.writerow(csv_values)
			#yield Request(next_page, callback=self.parse)
