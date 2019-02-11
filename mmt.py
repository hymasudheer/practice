import datetime
import os
import csv

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider

class Makemytrip(BaseSpider):
	
	name = "mmt"
	start_urls = ['https://www.makemytrip.com/blog/romantic-places']
	
	def __init__(self):
		self.filename = "mmtromantic%s.csv" % (str(datetime.datetime.now().date()))
		self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["blog_url", "blog_title", "image", "places_to visit"]
		self.csv_file.writerow(self.fields)
		
	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
			os.system('rm%s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file
	
	def parse(self, response):
		if self.start_urls[0] == response.url:
			counter = 0
		else:
			counter = response.meta.get('counter', 0)+1
		print (response.url)
		'''Node starts here'''
		sel = Selector(response)
		nodes= sel.xpath('//div[@class="category_part col-sm-4 col-xs-12"]')
		for node in nodes:
			blog_url = ''.join(node.xpath('.//p[@class="din-ab text_partinfo search_blog_title append_bottom8"]/a/@href').extract())
			blog_title = ''.join(node.xpath('.//p[@class="din-ab text_partinfo search_blog_title append_bottom8"]/a /text()').extract())
			image = node.xpath('./p[@class="append_bottom15"]/a/img/@data-src').extract()
			published_on = ("".join(node.xpath('.//div[@class="tile_detail_section append_bottom12"]/p[@class="din-ab text_sub_partinfo"]/text()').extract())).replace('\n\n', '')
			next_page = ''.join(sel.xpath('//ul[@class="pagination pagination-lg"]//li[@class="active"]/following-sibling::li[1][not(contains(@class, "disabled"))]/a/@href').extract())
			yield Request(blog_url, callback=self.parse_next, meta={'blog_url':blog_url, 'blog_title':blog_title, 'image':image, 'published_on':published_on,'next_page':next_page})
			#import pdb;pdb.set_trace()
	
	def parse_next(self, response):
		sel = Selector(response)
		blog_url = response.meta['blog_url']
		blog_title = response.meta['blog_title']
		image = response.meta['image']
		published_on = response.meta['published_on']
		next_page = response.meta['next_page']
		places_to_see = (','.join(sel.xpath('//div[@class="container body_container"]//h2/text()').extract())).replace('\r\n\t','')
		if next_page is not None:
			yield Request(next_page, callback=self.parse)
		csv_values = [blog_url, blog_title, image, places_to_see]
		self.csv_file.writerow(csv_values)
	